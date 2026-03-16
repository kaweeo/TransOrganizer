from decimal import Decimal
from django import template

register = template.Library()


@register.filter
def currency(value):
    if value is None:
        return "-"
    try:
        return f"{Decimal(value):.2f} €"
    except Exception:
        return value


@register.filter
def badge_class(status):
    mapping = {
        "pending": "bg-warning text-dark",
        "assigned": "bg-info text-dark",
        "in_transit": "bg-primary",
        "delivered": "bg-success",
        "cancelled": "bg-secondary",
    }
    return mapping.get(status, "bg-light text-dark")


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.simple_tag
def nav_active(request, prefix):
    if not request:
        return ""
    path = request.path or ""
    if path == prefix or path.startswith(prefix):
        return "active"
    return ""


@register.simple_tag
def nav_active_exact(request, path_value):
    if not request:
        return ""
    return "active" if request.path == path_value else ""


@register.simple_tag
def nav_active_prefix(request, prefix, exclude=None):
    if not request:
        return ""
    path = request.path or ""
    if exclude and path == exclude:
        return ""
    return "active" if path.startswith(prefix) else ""
