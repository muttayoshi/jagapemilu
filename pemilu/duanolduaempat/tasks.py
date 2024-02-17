from config import celery_app
from pemilu.duanolduaempat.utils import anomaly_detection, crawling_kpu
from pemilu.locations.models import Provinsi


@celery_app.task()
def crawling_all_kpu():
    provinsi = Provinsi.objects.all()
    for p in provinsi:
        crawling_kpu(p.code)


@celery_app.task()
def crawling_sumatera():
    provinsi = Provinsi.objects.filter(code__startswith="1").all()
    for p in provinsi:
        crawling_kpu(p.code)


@celery_app.task()
def crawling_riau():
    provinsi = Provinsi.objects.filter(code__startswith="2").all()
    for p in provinsi:
        crawling_kpu(p.code)


@celery_app.task()
def crawling_jawa():
    provinsi = Provinsi.objects.filter(code__startswith="3").all()
    for p in provinsi:
        crawling_kpu(p.code)


@celery_app.task()
def crawling_bali():
    provinsi = Provinsi.objects.filter(code__startswith="5").all()
    for p in provinsi:
        crawling_kpu(p.code)


@celery_app.task()
def crawling_kalimantan():
    provinsi = Provinsi.objects.filter(code__startswith="6").all()
    for p in provinsi:
        crawling_kpu(p.code)


@celery_app.task()
def crawling_sulawesi():
    provinsi = Provinsi.objects.filter(code__startswith="7").all()
    for p in provinsi:
        crawling_kpu(p.code)


@celery_app.task()
def crawling_maluku():
    provinsi = Provinsi.objects.filter(code__startswith="8").all()
    for p in provinsi:
        crawling_kpu(p.code)


@celery_app.task()
def crawling_papua():
    provinsi = Provinsi.objects.filter(code__startswith="9").all()
    for p in provinsi:
        crawling_kpu(p.code)


@celery_app.task()
def run_anomaly_detection():
    anomaly_detection()
