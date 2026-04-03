from celery import shared_task

from common.services.fuel_prices import update_croatia_prices


@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def update_croatia_fuel_prices(self):
    try:
        return update_croatia_prices()
        
    except Exception as exc:
        raise self.retry(exc=exc)
