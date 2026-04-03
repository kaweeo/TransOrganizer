import json
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings

from common.models import FuelPriceSnapshot, FuelType


FUEL_FIELD_MAP = {
    "gasoline": FuelType.GASOLINE,
    "diesel": FuelType.DIESEL,
}


def _normalize_collectapi_key(api_key):
    if not api_key:
        raise ValueError("COLLECTAPI_API_KEY is not set")

    cleaned = str(api_key).strip()
    if not cleaned:
        raise ValueError("COLLECTAPI_API_KEY is not set")

    # CollectAPI expects "apikey <key>", but allow callers to pass either
    # the full header value or just the raw key.
    if " " in cleaned:
        return cleaned

    return f"apikey {cleaned}"


def _parse_price(value):
    if value in (None, "", "-"):
        return None

    normalized = str(value).replace(",", ".")
    try:
        return Decimal(normalized)

    except (InvalidOperation, ValueError, TypeError):
        return None


def fetch_collectapi_prices():
    api_key = _normalize_collectapi_key(settings.COLLECTAPI_API_KEY)

    base_url = settings.COLLECTAPI_BASE_URL.rstrip("/")
    url = f"{base_url}/gasPrice/europeanCountries"

    headers = {
        "accept": "application/json",
        "authorization": api_key,
        "user-agent": "TransOrganizer/1.0",
    }

    request = Request(url, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=settings.COLLECTAPI_TIMEOUT) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        details = None
        try:
            body = exc.read().decode("utf-8")
        except Exception:
            body = ""
        if body:
            try:
                details = json.loads(body)
            except json.JSONDecodeError:
                details = body

        message = f"CollectAPI request failed: HTTP {exc.code} {exc.reason}"
        if exc.code == 403:
            message += (
                " (check COLLECTAPI_API_KEY format: raw key or 'apikey <key>', "
                "and verify your CollectAPI subscription for this endpoint)"
            )
        if details:
            message += f" | response: {details}"
        raise RuntimeError(message) from exc
    except URLError as exc:
        raise RuntimeError(f"CollectAPI request failed: {exc}") from exc

    if not payload.get("success"):
        raise RuntimeError("CollectAPI response indicated failure")

    return payload.get("result", [])


def update_croatia_prices():
    results = fetch_collectapi_prices()
    bg = next(
        (item for item in results if str(item.get("country", "")).strip().lower() == "croatia"),
        None,
    )
    if not bg:
        raise RuntimeError("Croatia was not found in CollectAPI response")

    currency = bg.get("currency") or ""
    updated = 0

    for field, fuel_type in FUEL_FIELD_MAP.items():
        price = _parse_price(bg.get(field))
        if price is None:
            continue

        FuelPriceSnapshot.objects.filter(
            country__iexact="Croatia",
            fuel_type=fuel_type,
            is_current=True,
        ).update(is_current=False)

        FuelPriceSnapshot.objects.create(
            country="Croatia",
            currency=currency,
            fuel_type=fuel_type,
            price=price,
            source="collectapi",
            is_current=True,
            raw_payload=bg,
        )
        updated += 1

    return updated
