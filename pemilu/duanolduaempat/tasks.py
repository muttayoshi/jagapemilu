from config import celery_app
from celery import shared_task
from pemilu.duanolduaempat.utils import anomaly_detection, crawling_kpu, calculate_province_report
from pemilu.locations.models import Provinsi


@celery_app.task()
def crawling_all_kpu():
    provinsi = Provinsi.objects.all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_all_kpu"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def crawling_sumatera():
    provinsi = Provinsi.objects.filter(code__startswith="1").all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_sumatera"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def crawling_riau():
    provinsi = Provinsi.objects.filter(code__startswith="2").all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_riau"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def crawling_jawa():
    provinsi = Provinsi.objects.filter(code__startswith="3").all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_jawa"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def crawling_bali():
    provinsi = Provinsi.objects.filter(code__startswith="5").all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_bali"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def crawling_kalimantan():
    provinsi = Provinsi.objects.filter(code__startswith="6").all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_kalimantan"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def crawling_sulawesi():
    provinsi = Provinsi.objects.filter(code__startswith="7").all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_sulawesi"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def crawling_maluku():
    provinsi = Provinsi.objects.filter(code__startswith="8").all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_maluku"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def crawling_papua():
    provinsi = Provinsi.objects.filter(code__startswith="9").all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_papua"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def crawling_select_province(province_code):
    provinsi = Provinsi.objects.filter(code__startswith=province_code).all()
    for p in provinsi:
        crawling_kpu(p.code)
    return f"crawling_province_code{province_code}"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def run_anomaly_detection():
    anomaly_detection()
    return "run_anomaly_detection"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def run_calculate_province_report():
    calculate_province_report()
    return "run_calculate_province_report"
    
