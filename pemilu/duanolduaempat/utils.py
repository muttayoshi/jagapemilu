import requests
from django.db.models import Sum

from pemilu.duanolduaempat.models import Administration, AnomalyDetection, Chart, Image, Report, ReportDetail, Tps
from pemilu.locations.models import Kelurahan, Provinsi


def crawling_kpu(province_code):
    list_province_code = province_code.split(",")
    for province in list_province_code:
        prov_id = Provinsi.objects.get(code=province)
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
                                "province": prov_id,
                            },
                        )

                        if created:
                            print(f"TPS: {datatps}")

                            data_chart = data["chart"]
                            if data_chart:
                                for key, value in data_chart.items():
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
                        else:
                            if datatps.has_anomaly:
                                print(f"TPS: {datatps}")

                                data_chart = data["chart"]
                                if data_chart:
                                    for key, value in data_chart.items():
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


def anomaly_detection():
    result = []
    AnomalyDetection.objects.all().delete()
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
                    result.append(
                        {
                            "url": t.url,
                            "message": f"Suara Sah: {suara_sah} higher than Suara Total: {suara_total} - "
                            f"Anomaly Detected",
                            "type": "System Error",
                        }
                    )
                    error += 1

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
                    result.append(
                        {
                            "url": t.url,
                            "message": f"Count: {c.count} higher than 300 - Anomaly Detected",
                            "type": "Human Error",
                        }
                    )
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
                result.append(
                    {
                        "url": t.url,
                        "message": f"Count: {count} does not match with Suara Sah: {suara_sah} - Anomaly Detected",
                        "type": "System Error",
                    }
                )

    print("Anomaly Detection Done")
    print(f"Total Anomaly Detected: {error}")
    return {"message": "Anomaly Detection Done", "total_anomaly_detected": error, "result": result}


def calculate_percentage_detail():
    tps_correct = Tps.objects.filter(status_suara=True, status_adm=True, has_anomaly=False)
    A100025 = Chart.objects.filter(
        name="100025", tps__status_suara=True, tps__status_adm=True, tps__has_anomaly=False
    ).aggregate(Sum("count"))
    A100026 = Chart.objects.filter(
        name="100026", tps__status_suara=True, tps__status_adm=True, tps__has_anomaly=False
    ).aggregate(Sum("count"))
    A100027 = Chart.objects.filter(
        name="100027", tps__status_suara=True, tps__status_adm=True, tps__has_anomaly=False
    ).aggregate(Sum("count"))
    total = A100025.get("count__sum") + A100026.get("count__sum") + A100027.get("count__sum")
    anies = A100025.get("count__sum")

    prabowo = A100026.get("count__sum")

    ganjar = A100027.get("count__sum")

    anies_p = f"{(anies / total) * 100} %"

    prabowo_p = f"{(prabowo / total) * 100} %"

    ganjar_p = f"{(ganjar / total) * 100}%"

    Report.objects.update_or_create(
        name="Pemilu 2024",
        defaults={
            "total_suara": total,
            "total_tps": tps_correct.count(),
            "paslon_satu": anies,
            "paslon_dua": prabowo,
            "paslon_tiga": ganjar,
        },
    )

    result = {
        "tps_correct": tps_correct.count(),
        "total_suara": total,
        "suara_anies": anies,
        "suara_prabowo": prabowo,
        "suara_ganjar": ganjar,
        "percentage_anies": anies_p,
        "percentage_prabowo": prabowo_p,
        "percentage_ganjar": ganjar_p,
    }
    return result


def calculate_percentage():
    tps_correct = Tps.objects.filter(status_suara=True, status_adm=True, has_anomaly=False).count()
    candidates = ["100025", "100026", "100027"]
    votes = {
        candidate: Chart.objects.filter(
            name=candidate, tps__status_suara=True, tps__status_adm=True, tps__has_anomaly=False
        )
        .aggregate(Sum("count"))
        .get("count__sum")
        for candidate in candidates
    }
    total_votes = sum(votes.values())
    percentages = {candidate: f"{(votes[candidate] / total_votes) * 100} %" for candidate in candidates}

    result = {
        "tps_correct": tps_correct,
        "total_suara": total_votes,
    }
    result.update(votes)
    result.update(percentages)
    return result


def set_provice_code():
    tps = Tps.objects.all()
    for t in tps:
        province_code = t.name[:2]
        t.province = Provinsi.objects.get(code=province_code)
        t.save()


def calculate_province_report():
    provinces = Provinsi.objects.all()
    for province in provinces:
        tps_correct = Tps.objects.filter(
            province=province, status_suara=True, status_adm=True, has_anomaly=False
        ).all()
        print(tps_correct.count())
        report = Report.objects.filter(name="Pemilu 2024").first()
        print(report)
        if report and tps_correct:
            total_suara = 0
            total_tps = 0
            paslon_satu = 0
            paslon_dua = 0
            paslon_tiga = 0
            for tps in tps_correct:
                tps_count = tps.charts.filter(is_deleted=False).aggregate(Sum("count")).get("count__sum")
                if tps_count and tps_count > 0:
                    total_tps += 1
                    total_suara += tps_count
                    satu = tps.charts.filter(name="100025", is_deleted=False).last()
                    if satu:
                        paslon_satu += satu.count
                    dua = tps.charts.filter(name="100026", is_deleted=False).last()
                    if dua:
                        paslon_dua += dua.count
                    tiga = tps.charts.filter(name="100027", is_deleted=False).last()
                    if tiga:
                        paslon_tiga += tiga.count
            ReportDetail.objects.update_or_create(
                report=report,
                province=province,
                defaults={
                    "total_suara": total_suara,
                    "total_tps": total_tps,
                    "paslon_satu": paslon_satu,
                    "paslon_dua": paslon_dua,
                    "paslon_tiga": paslon_tiga,
                },
            )
