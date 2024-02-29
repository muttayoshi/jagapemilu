from config import celery_app
from pemilu.locations.utils import update_data_province


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def update_province():
    update_data_province()
    return "update_province"
