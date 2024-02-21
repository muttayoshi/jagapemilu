from config import celery_app
from pemilu.duanolduaempat.utils import calculate_province_report, crawling_kpu, migration_ts, calculate_percentage_detail, divide_data
from pemilu.locations.models import Provinsi
from pemilu.duanolduaempat.models import Tps, AnomalyDetection, Image
from pemilu.utils.storages import S3Storage


@celery_app.task()
def crawling_all_kpu():
    provinsi = Provinsi.objects.all()
    for p in provinsi:
        crawling_kpu(p.code)
    return "crawling_all_kpu"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def anomaly_detection(id_min, id_max):
    if id_min and id_max:
        tps = Tps.objects.filter(id__gte=id_min, id__lte=id_max)
    else:
        tps = Tps.objects.all()
    error = 0
    for t in tps:
        if t.status_adm and t.status_suara:
            charts = t.charts.filter(is_deleted=False).all()
            administrations = t.administrations.last()
            suara_sah = 0
            is_clean = True
            if administrations:
                suara_sah = administrations.suara_sah
                suara_total = administrations.suara_total

                if suara_sah and suara_total and suara_sah > suara_total:
                    AnomalyDetection.objects.create(
                        tps=t,
                        url=t.url,
                        message=f"Suara Sah: {suara_sah} lebih banyak daripada Suara Total: {suara_total} - ",
                        type="Suara sah lebih besar dari total suara",
                        ts=t.ts,
                    )
                    is_clean = False

            count = 0
            for c in charts:
                if c.count and c.count > 300:
                    if c.name == "100025":
                        paslon_name = "Anies"
                    elif c.name == "100026":
                        paslon_name = "Prabowo"
                    elif c.name == "100027":
                        paslon_name = "Ganjar"
                    else:
                        paslon_name = "Unknown"
                    AnomalyDetection.objects.create(
                        tps=t,
                        url=t.url,
                        message=f"Suara pada paslon {paslon_name} bernilai {c.count}, lebih tinggi dari 300",
                        type=f"Overload {paslon_name}",
                        ts=t.ts,
                    )
                    is_clean = False
                if c.count:
                    count += c.count

            if suara_sah and count != suara_sah:
                AnomalyDetection.objects.create(
                    tps=t,
                    url=t.url,
                    message=f"Jumlah total suara {count} tidak cocok dengan suara aah: {suara_sah}",
                    type="Jumlah suara sah tidak cocok",
                )
                is_clean = False

            if is_clean:
                t.has_anomaly = False
                t.save()
            else:
                error += 1

    return {"message": "Anomaly Detection Done", "total_anomaly_detected": error}


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
    tps_count = Tps.objects.count()
    id_range = divide_data(tps_count, 3)
    for i in id_range:
        anomaly_detection.delay(i[0], i[1])
    return "run_anomaly_detection"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def run_calculate_province_report():
    calculate_province_report()
    return "run_calculate_province_report"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def run_migration_ts():
    tps_count = Tps.objects.count()
    id_range = divide_data(tps_count, 3)
    for i in id_range:
        call_migration_ts.delay(i[0], i[1])
    return "run_migration_ts"

@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def call_migration_ts(id_min, id_max):
    migration_ts(id_min, id_max)
    return "run_migration_ts"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def backup_chasil_image():
    chasil_count = Image.objects.count()
    id_range = divide_data(chasil_count, 3)
    for i in id_range:
        id_min = i[0]
        id_max = i[1]
        upload_s3_image.delay(id_min, id_max)
    return "backup_chasil_image"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def upload_s3_image(id_min, id_max):
    storage = S3Storage()
    for image_id in range(id_min, id_max):
        storage.backup_image(image_id)
    return
