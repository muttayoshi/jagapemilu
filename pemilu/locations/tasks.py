from config import celery_app
from pemilu.locations.utils import update_data_province


@celery_app.task()
def update_province():
    update_data_province()
    return "update_province"
