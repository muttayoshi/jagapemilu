import requests
from celery import shared_task

from pemilu.duanolduaempat.models import Administration, AnomalyDetection, Chart, Image, Tps
from pemilu.locations.models import Kelurahan, Provinsi


@shared_task
def crawling_all_kpu():
    provinsi = Provinsi.objects.all()
    for p in provinsi:
        crawling_kpu(p.code)


@shared_task
def crawling_sumatera():
    provinsi = Provinsi.objects.filter(code__startswith="1").all()
    for p in provinsi:
        crawling_kpu(p.code)


@shared_task
def crawling_riau():
    provinsi = Provinsi.objects.filter(code__startswith="2").all()
    for p in provinsi:
        crawling_kpu(p.code)


@shared_task
def crawling_jawa():
    provinsi = Provinsi.objects.filter(code__startswith="3").all()
    for p in provinsi:
        crawling_kpu(p.code)


@shared_task
def crawling_bali():
    provinsi = Provinsi.objects.filter(code__startswith="5").all()
    for p in provinsi:
        crawling_kpu(p.code)


@shared_task
def crawling_kalimantan():
    provinsi = Provinsi.objects.filter(code__startswith="6").all()
    for p in provinsi:
        crawling_kpu(p.code)


@shared_task
def crawling_sulawesi():
    provinsi = Provinsi.objects.filter(code__startswith="7").all()
    for p in provinsi:
        crawling_kpu(p.code)


@shared_task
def crawling_maluku():
    provinsi = Provinsi.objects.filter(code__startswith="8").all()
    for p in provinsi:
        crawling_kpu(p.code)


@shared_task
def crawling_papua():
    provinsi = Provinsi.objects.filter(code__startswith="9").all()
    for p in provinsi:
        crawling_kpu(p.code)


def crawling_kpu(province_code):
    list_province_code = province_code.split(",")
    for province in list_province_code:
        kelurahan = Kelurahan.objects.filter(code__startswith=province).all()
        print(kelurahan.first())

        for k in kelurahan:
            kelurahan = k.code
            kecamatan = kelurahan[:-4]
            kota = kecamatan[:-2]
            provinsi = kota[:-2]

            tps = "001"
            while True:
                print(
                    f"Provinsi: {provinsi}, Kota: {kota}, Kecamatan: {kecamatan}, Kelurahan: {kelurahan}, TPS: {tps}"
                )
                try:
                    url = (
                        f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/"
                        f"{provinsi}/{kota}/{kecamatan}/{kelurahan}/{kelurahan}{tps}.json"
                    )

                    payload = {}
                    headers = {}

                    response = requests.request("GET", url, headers=headers, data=payload)

                    if response.status_code == 200:
                        data = response.json()
                        datatps, created = Tps.objects.update_or_create(
                            name=f"{kelurahan}{tps}",
                            defaults={
                                "psu": data["psu"],
                                "ts": data["ts"],
                                "status_suara": data["status_suara"],
                                "status_adm": data["status_adm"],
                                "url": f"https://pemilu2024.kpu.go.id/pilpres/hitung-suara/"
                                f"{provinsi}/{kota}/{kecamatan}/{kelurahan}/{kelurahan}{tps}",
                            },
                        )

                        print(f"TPS: {datatps}, Created: {created}")

                        data_chart = data["chart"]
                        if data_chart:
                            for key, value in data_chart.items():
                                # Chart.objects.update_or_create(
                                #     tps=datatps,
                                #     name=key,
                                #     defaults={
                                #         'count': value
                                #     }
                                # )
                                Chart.objects.filter(tps=datatps, name=key).update(is_deleted=True)
                                Chart.objects.create(tps=datatps, name=key, count=value)

                        data_image = data["images"]
                        for image in data_image:
                            Image.objects.get_or_create(tps=datatps, url=image)

                        if data.get("administrasi"):
                            value = data.get("administrasi")
                            Administration.objects.update_or_create(
                                tps=datatps,
                                defaults={
                                    "suara_sah": value.get("suara_sah"),
                                    "suara_total": value.get("suara_total"),
                                    "pemilih_dpt_l": value.get("pemilih_dpt_l"),
                                    "pemilih_dpt_p": value.get("pemilih_dpt_p"),
                                    "pengguna_dpt_j": value.get("pengguna_dpt_j"),
                                    "pengguna_dpt_l": value.get("pengguna_dpt_l"),
                                    "pengguna_dpt_p": value.get("pengguna_dpt_p"),
                                    "pengguna_dptb_j": value.get("pengguna_dptb_j"),
                                    "pengguna_dptb_l": value.get("pengguna_dptb_l"),
                                    "pengguna_dptb_p": value.get("pengguna_dptb_p"),
                                    "suara_tidak_sah": value.get("suara_tidak_sah"),
                                    "pengguna_total_j": value.get("pengguna_total_j"),
                                    "pengguna_total_l": value.get("pengguna_total_l"),
                                    "pengguna_total_p": value.get("pengguna_total_p"),
                                    "pengguna_non_dpt_j": value.get("pengguna_non_dpt_j"),
                                    "pengguna_non_dpt_l": value.get("pengguna_non_dpt_l"),
                                    "pengguna_non_dpt_p": value.get("pengguna_non_dpt_p"),
                                },
                            )
                    elif response.status_code == 404:
                        print("TPS NOT FOUND")
                        break
                    else:
                        print("Failed to get data from URL")
                except Exception as e:
                    print(e)
                tps = str(int(tps) + 1).zfill(3)


@shared_task
def anomaly_detection():
    tps = Tps.objects.all()

    error = 0
    for t in tps:
        if t.status_adm and t.status_suara:
            charts = t.charts.filter(is_deleted=False).all()
            administrations = t.administrations.last()
            suara_sah = 0
            if administrations:
                suara_sah = administrations.suara_sah
                suara_total = administrations.suara_total

                if suara_sah and suara_total and suara_sah > suara_total:
                    AnomalyDetection.objects.get_or_create(
                        tps=t,
                        url=t.url,
                        message=f"Suara Sah: {suara_sah} higher than Suara Total: {suara_total} - Anomaly Detected",
                        type="System Error",
                    )
                    t.has_anomaly = True
                    t.save()
                    print(
                        f"Suara Sah: {suara_sah} higher than Suara Total: {suara_total} "
                        f"- Anomaly Detected (Human Error)"
                    )
                    error += 1
                    print(f"TPS: {t.url}")

            count = 0
            for c in charts:
                if c.count and c.count > 300:
                    AnomalyDetection.objects.get_or_create(
                        tps=t,
                        url=t.url,
                        message=f"Count: {c.count} higher than 300 - Anomaly Detected",
                        type="Human Error",
                    )
                    t.has_anomaly = True
                    t.save()
                    error += 1
                    print(f"Count: {c.count} higher than 300 - Anomaly Detected (Curang)")
                    print(f"TPS: {t.url}")
                if c.count:
                    count += c.count

            if suara_sah and count != suara_sah:
                AnomalyDetection.objects.get_or_create(
                    tps=t,
                    url=t.url,
                    message=f"Count: {count} does not match with Suara Sah: {suara_sah} - Anomaly Detected",
                    type="System Error",
                )
                error += 1
                t.has_anomaly = True
                t.save()
                print(f"Count: {count} does not match with Suara Sah: {suara_sah} - Anomaly Detected (Human Error)")
                print(f"TPS: {t.url}")

    print("Anomaly Detection Done")
    print(f"Total Anomaly Detected: {error}")
