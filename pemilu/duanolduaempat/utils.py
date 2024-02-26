from datetime import datetime

import requests
from django.db.models import Sum

from pemilu.duanolduaempat.models import (
    Administration,
    AnomalyDetection,
    BackupCHasil,
    Chart,
    Image,
    Report,
    ReportDetail,
    Tps,
)
from pemilu.locations.models import Kelurahan, Provinsi


def crawling_kpu(province_code):
    list_province_code = province_code.split(",")
    for province in list_province_code:
        prov_id = Provinsi.objects.get(code=province)
        kelurahan = Kelurahan.objects.filter(code__startswith=province).all()

        for k in kelurahan:
            kelurahan = k.code
            kecamatan = kelurahan[:-4]
            kota = kecamatan[:-2]
            provinsi = kota[:-2]

            tps = "001"
            while True:
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
                                "kelurahan": k,
                                "has_anomaly": True,
                            },
                        )

                        data_chart = data["chart"]
                        if data_chart:
                            for key, value in data_chart.items():
                                chart, chart_created = Chart.objects.get_or_create(
                                    tps=datatps, name=key, count=value, ts=data["ts"]
                                )
                                if chart_created:
                                    Chart.objects.filter(tps=datatps, name=key).exclude(id=chart.id).update(
                                        is_deleted=True
                                    )

                        data_image = data["images"]
                        for image in data_image:
                            Image.objects.get_or_create(
                                tps=datatps,
                                ts=data["ts"],
                                url=image,
                            )

                        if data.get("administrasi"):
                            value = data.get("administrasi")
                            Administration.objects.update_or_create(
                                tps=datatps,
                                ts=data["ts"],
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
            if t.name[:2] != "99":
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
                    message=f"Jumlah total suara {count} tidak cocok dengan suara sah: {suara_sah}",
                    type="Jumlah suara sah tidak cocok",
                )
                is_clean = False

            if is_clean:
                t.has_anomaly = False
                t.save()
            else:
                error += 1

    return {"message": "Anomaly Detection Done", "total_anomaly_detected": error}


def calculate_percentage_detail():
    tps_correct = Tps.objects.filter(status_suara=True, status_adm=True, has_anomaly=False)

    # total_suara_h3 = 0
    # for tps in tps_correct:
    #     try:
    #         data_adm = tps.administrations.last()
    #         if data_adm:
    #             total_suara_h3 += data_adm.suara_sah
    #     except:
    #         print(tps.name)

    # total_suara_h3 = sum(tps.administrations.last().suara_sah for tps in tps_correct if tps.administrations.last())
    # satu
    total_suara_h3 = sum(
        (tps.administrations.last().suara_sah or 0) for tps in tps_correct if tps.administrations.last()
    )

    candidates = ["100025", "100026", "100027"]
    votes = {
        candidate: Chart.objects.filter(
            name=candidate, tps__status_suara=True, tps__status_adm=True, tps__has_anomaly=False, is_deleted=False
        )
        .aggregate(Sum("count"))
        .get("count__sum")
        for candidate in candidates
    }
    total_votes = sum(votes.values())

    percentages = {f"{candidate}_p": f"{(votes[candidate] / total_votes) * 100} %" for candidate in candidates}

    Report.objects.update_or_create(
        name="Pemilu 2024",
        defaults={
            "total_suara": total_votes,
            "total_suara_h_3": total_suara_h3,
            "total_tps": tps_correct.count(),
            "paslon_satu": votes["100025"],
            "paslon_dua": votes["100026"],
            "paslon_tiga": votes["100027"],
        },
    )

    result = {
        "tps_correct": tps_correct.count(),
        "total_suara": total_votes,
    }
    result.update(votes)
    result.update(percentages)
    return result


def calculate_percentage_detail_for_anomaly_tps():
    tps_anomaly = Tps.objects.filter(status_suara=True, status_adm=True, has_anomaly=True)

    # total_suara_h3 = 0
    # for tps in tps_anomaly:
    #     try:
    #         data_adm = tps.administrations.last()
    #         if data_adm:
    #             total_suara_h3 += data_adm.suara_sah
    #     except:
    #         print(tps.name)
    # dua
    total_suara_h3 = sum(
        (tps.administrations.last().suara_sah or 0) for tps in tps_anomaly if tps.administrations.last()
    )

    candidates = ["100025", "100026", "100027"]
    votes = {
        candidate: Chart.objects.filter(
            name=candidate, tps__status_suara=True, tps__status_adm=True, tps__has_anomaly=True, is_deleted=False
        )
        .aggregate(Sum("count"))
        .get("count__sum")
        for candidate in candidates
    }
    total_votes = sum(votes.values())
    percentages = {f"{candidate}_p": f"{(votes[candidate] / total_votes) * 100} %" for candidate in candidates}

    Report.objects.update_or_create(
        name="TPS Anomaly Report",
        defaults={
            "total_suara": total_votes,
            "total_suara_h_3": total_suara_h3,
            "total_tps": tps_anomaly.count(),
            "paslon_satu": votes["100025"],
            "paslon_dua": votes["100026"],
            "paslon_tiga": votes["100027"],
        },
    )

    result = {
        "tps_anomaly": tps_anomaly.count(),
        "total_suara": total_votes,
    }
    result.update(votes)
    result.update(percentages)
    return result


def set_province_code():
    tps = Tps.objects.all()
    for t in tps:
        province_code = t.name[:2]
        t.province = Provinsi.objects.get(code=province_code)
        t.save()


def set_kelurahan_code(id_min, id_max):
    if id_min and id_max:
        tps = Tps.objects.filter(id__gte=id_min, id__lte=id_max)
    else:
        tps = Tps.objects.all()
    for t in tps:
        kelurahan_code = t.name[:10]
        kelurahan = Kelurahan.objects.get(code=kelurahan_code)
        t.kelurahan = kelurahan
        t.save()

        images = t.images.all()
        for image in images:
            image.kelurahan = kelurahan
            image.save()


def calculate_province_report():
    calculate_percentage_detail()
    provinces = Provinsi.objects.all()
    report = Report.objects.filter(name="Pemilu 2024").first()

    for province in provinces:
        tps_correct = Tps.objects.filter(province=province, status_suara=True, status_adm=True, has_anomaly=False)

        if report and tps_correct.exists():
            total_suara, total_tps, paslon_satu, paslon_dua, paslon_tiga = 0, 0, 0, 0, 0

            suara_sah_h3 = 0
            for tps in tps_correct:
                data_adm = tps.administrations.last()
                if data_adm and data_adm.suara_sah:
                    suara_sah_h3 += data_adm.suara_sah

                tps_count = tps.charts.filter(is_deleted=False).aggregate(Sum("count")).get("count__sum")
                if tps_count and tps_count > 0:
                    total_tps += 1
                    total_suara += tps_count
                    count_paslon_satu = tps.charts.filter(name="100025", is_deleted=False).last()
                    paslon_satu += count_paslon_satu.count if count_paslon_satu else 0
                    count_paslon_dua = tps.charts.filter(name="100026", is_deleted=False).last()
                    paslon_dua += count_paslon_dua.count if count_paslon_dua else 0
                    count_paslon_tiga = tps.charts.filter(name="100027", is_deleted=False).last()
                    paslon_tiga += count_paslon_tiga.count if count_paslon_tiga else 0
            # tiga
            # suara_sah_h3 = sum(
            #     (tps.administrations.last().suara_sah or 0) for tps in tps_correct if tps.administrations.last()
            # )
            # total_tps = sum(
            #     1
            #     for tps in tps_correct
            #     if tps.charts.filter(is_deleted=False).aggregate(Sum("count")).get("count__sum") > 0
            # )
            # total_suara = sum(
            #     tps.charts.filter(is_deleted=False).aggregate(Sum("count")).get("count__sum") for tps in tps_correct
            # )
            # paslon_satu = sum(
            #     tps.charts.filter(name="100025", is_deleted=False).last().count or 0 for tps in tps_correct
            # )
            # paslon_dua = sum(
            #     tps.charts.filter(name="100026", is_deleted=False).last().count or 0 for tps in tps_correct
            # )
            # paslon_tiga = sum(
            #     tps.charts.filter(name="100027", is_deleted=False).last().count or 0 for tps in tps_correct
            # )

            ReportDetail.objects.update_or_create(
                report=report,
                province=province,
                defaults={
                    "total_suara": total_suara,
                    "total_suara_h_3": suara_sah_h3,
                    "total_tps": total_tps,
                    "paslon_satu": paslon_satu,
                    "paslon_dua": paslon_dua,
                    "paslon_tiga": paslon_tiga,
                },
            )
    return {"message": "Percentage Detail Done"}


def calculate_province_anomaly_tps_report():
    calculate_percentage_detail_for_anomaly_tps()
    provinces = Provinsi.objects.all()
    report = Report.objects.filter(name="TPS Anomaly Report").first()

    for province in provinces:
        tps_correct = Tps.objects.filter(province=province, status_suara=True, status_adm=True, has_anomaly=True).all()

        if report and tps_correct:
            total_suara, total_tps, paslon_satu, paslon_dua, paslon_tiga = 0, 0, 0, 0, 0

            total_suara_h3 = 0
            for tps in tps_correct:
                data_adm = tps.administrations.last()
                if data_adm and data_adm.suara_sah:
                    total_suara_h3 += data_adm.suara_sah


                tps_count = tps.charts.filter(is_deleted=False).aggregate(Sum("count")).get("count__sum")
                if tps_count and tps_count > 0:
                    total_tps += 1
                    total_suara += tps_count

                    if tps.charts.filter(name="100025", is_deleted=False).last():
                        paslon_satu += tps.charts.filter(name="100025", is_deleted=False).last().count or 0
                    if tps.charts.filter(name="100026", is_deleted=False).last():
                        paslon_dua += tps.charts.filter(name="100026", is_deleted=False).last().count or 0
                    if tps.charts.filter(name="100027", is_deleted=False).last():
                        paslon_tiga += tps.charts.filter(name="100027", is_deleted=False).last().count or 0

            #         # paslon_satu += tps.charts.filter(name="100025", is_deleted=False).last().count or 0
            #         # paslon_dua += tps.charts.filter(name="100026", is_deleted=False).last().count or 0
            #         # paslon_tiga += tps.charts.filter(name="100027", is_deleted=False).last().count or 0

            # total_suara_h3 = sum(
            #     tps.administrations.last().suara_sah or 0 for tps in tps_correct if tps.administrations.last()
            # )
            # total_tps = sum(
            #     1
            #     for tps in tps_correct
            #     if tps.charts.filter(is_deleted=False).aggregate(Sum("count")).get("count__sum") > 0
            # )
            # total_suara = sum(
            #     tps.charts.filter(is_deleted=False).aggregate(Sum("count")).get("count__sum") for tps in tps_correct
            # )
            # paslon_satu = sum(
            #     tps.charts.filter(name="100025", is_deleted=False).last().count or 0 for tps in tps_correct
            # )
            # paslon_dua = sum(
            #     tps.charts.filter(name="100026", is_deleted=False).last().count or 0 for tps in tps_correct
            # )
            # paslon_tiga = sum(
            #     tps.charts.filter(name="100027", is_deleted=False).last().count or 0 for tps in tps_correct
            # )

            ReportDetail.objects.update_or_create(
                report=report,
                province=province,
                defaults={
                    "total_suara": total_suara,
                    "total_suara_h_3": total_suara_h3,
                    "total_tps": total_tps,
                    "paslon_satu": paslon_satu,
                    "paslon_dua": paslon_dua,
                    "paslon_tiga": paslon_tiga,
                },
            )
    return {"message": "Percentage Detail Done"}


def migration_ts(id_min=None, id_max=None):
    if id_min and id_max:
        tps = Tps.objects.filter(id__gte=id_min, id__lte=id_max)
    else:
        tps = Tps.objects.all()
    for t in tps:
        charts = t.charts.filter(is_deleted=False).all()
        for c in charts:
            c.ts = t.ts
            c.save()
        images = t.images.all()
        for i in images:
            i.ts = t.ts
            i.save()
        administrations = t.administrations.last()
        if administrations:
            administrations.ts = t.ts
            administrations.save()


def update_tps(id_min, id_max):
    tps = Tps.objects.filter(id__gte=id_min, id__lte=id_max)
    for t in tps:
        url = t.url.replace(
            "https://pemilu2024.kpu.go.id/pilpres/hitung-suara/",
            "https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/",
        )

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json()
            datatps, created = Tps.objects.update_or_create(
                name=t.name,
                defaults={
                    "psu": data["psu"],
                    "ts": data["ts"],
                    "status_suara": data["status_suara"],
                    "status_adm": data["status_adm"],
                    "url": f"https://pemilu2024.kpu.go.id/pilpres/hitung-suara/"
                    f"{t.province.code}/{t.province.kota.code}/{t.province.kota.kecamatan.code}/"
                    f"{t.province.kota.kecamatan.kelurahan.code}/{t.name}",
                },
            )

            data_chart = data["chart"]
            if data_chart:
                for key, value in data_chart.items():
                    Chart.objects.filter(tps=datatps, name=key).update(is_deleted=True)
                    Chart.objects.create(tps=datatps, name=key, count=value, ts=data["ts"])

            data_image = data["images"]
            for image in data_image:
                Image.objects.get_or_create(
                    tps=datatps,
                    ts=data["ts"],
                    url=image,
                )

            if data.get("administrasi"):
                value = data.get("administrasi")
                Administration.objects.update_or_create(
                    tps=datatps,
                    ts=data["ts"],
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
        else:
            print("Failed to get data from URL")


def divide_data(total_data, num_parts):
    part_size = total_data // num_parts
    remainder = total_data % num_parts
    result = []
    start = 1
    for i in range(num_parts):
        end = start + part_size - 1
        if remainder > 0:
            end += 1
            remainder -= 1
        result.append((start, end))
        start = end + 1
    return result


def rename_s3url():
    date_object = datetime.strptime("2024-02-22 09:00:00", "%Y-%m-%d %H:%M:%S")
    backups = BackupCHasil.objects.filter(created__gte=date_object).all()
    for backup in backups:
        backup.s3_url = backup.s3_url.replace("fc924094dd6f45899cb57557bc79b15d", "3e6fed6b6c9b4ce8bb143ddd4481477e")
        backup.save()
