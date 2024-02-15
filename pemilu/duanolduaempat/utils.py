import requests
import json


from pemilu.locations.models import Provinsi, Kota, Kecamatan, Kelurahan
from pemilu.duanolduaempat.models import Tps, Chart, Image, Administration, AnomalyDetection

def crawling_kpu_v1(province_code):

    # kelurahan = Kelurahan.objects.all()
    kelurahan = Kelurahan.objects.filter(code__startswith=province_code).all()

    for k in kelurahan:
        kelurahan = k.code
        kecamatan = kelurahan[:-4]
        kota = kecamatan[:-2]
        provinsi = kota[:-2]

        tps = "001"
        while True:
            print(f"Provinsi: {provinsi}, Kota: {kota}, Kecamatan: {kecamatan}, Kelurahan: {kelurahan}, TPS: {tps}")
            try:
                url = f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/{provinsi}/{kota}/{kecamatan}/{kelurahan}/{kelurahan}{tps}.json"

                payload = {}
                headers = {}

                response = requests.request("GET", url, headers=headers, data=payload)

                # print(response.status_code)

                if response.status_code == 200:
                    data = response.json()
                    datatps, created = Tps.objects.get_or_create(
                        name=f"{kelurahan}{tps}",
                        psu=data['psu'],
                        ts=data['ts'],
                        status_suara=data['status_suara'],
                        status_adm=data['status_adm'],
                        url=f"https://pemilu2024.kpu.go.id/pilpres/hitung-suara/{provinsi}/{kota}/{kecamatan}/{kelurahan}/{kelurahan}{tps}"
                    )

                    print(f"TPS: {datatps}, Created: {created}")

                    data_chart = data['chart']
                    if data_chart:
                        for key, value in data_chart.items():
                            Chart.objects.get_or_create(
                                tps=datatps,
                                name=key,
                                count=value
                            )

                    data_image = data['images']
                    for image in data_image:
                        Image.objects.get_or_create(
                            tps=datatps,
                            url=image
                        )

                    if data.get("administrasi"):
                        value = data.get("administrasi")
                        Administration.objects.get_or_create(
                            tps=datatps,
                            suara_sah=value.get('suara_sah'),
                            suara_total=value.get('suara_total'),
                            pemilih_dpt_l=value.get('pemilih_dpt_l'),
                            pemilih_dpt_p=value.get('pemilih_dpt_p'),
                            pengguna_dpt_j=value.get('pengguna_dpt_j'),
                            pengguna_dpt_l=value.get('pengguna_dpt_l'),
                            pengguna_dpt_p=value.get('pengguna_dpt_p'),
                            pengguna_dptb_j=value.get('pengguna_dptb_j'),
                            pengguna_dptb_l=value.get('pengguna_dptb_l'),
                            pengguna_dptb_p=value.get('pengguna_dptb_p'),
                            suara_tidak_sah=value.get('suara_tidak_sah'),
                            pengguna_total_j=value.get('pengguna_total_j'),
                            pengguna_total_l=value.get('pengguna_total_l'),
                            pengguna_total_p=value.get('pengguna_total_p'),
                            pengguna_non_dpt_j=value.get('pengguna_non_dpt_j'),
                            pengguna_non_dpt_l=value.get('pengguna_non_dpt_l'),
                            pengguna_non_dpt_p=value.get('pengguna_non_dpt_p')
                        )
                elif response.status_code == 404:
                    print("TPS NOT FOUND")
                    break
                else:
                    print("Failed to get data from URL")
                    # condition = False
            except Exception as e:
                print(e)
                # with open('pemilu.json', 'w') as f:
                #     json.dump(e, f, indent=4)

            tps = str(int(tps) + 1).zfill(3)


def anomaly_detection():
    tps = Tps.objects.all()

    for t in tps:
        if t.status_adm and t.status_suara:
            charts = t.charts.all()
            administrations = t.administrations.last()
            suara_sah = 0
            if administrations:
                suara_sah = administrations.suara_sah
                suara_total = administrations.suara_total

                if suara_sah and suara_total and suara_sah > suara_total:
                    AnomalyDetection.objects.get_or_create(
                        tps=t,
                        url = t.url,
                        message = f"Suara Sah: {suara_sah} higher than Suara Total: {suara_total} - Anomaly Detected",
                        type = "Human Error"
                    )
                    print(f"Suara Sah: {suara_sah} higher than Suara Total: {suara_total} - Anomaly Detected (Human Error)")
                    print(f"TPS: {t.url}")

            count = 0
            for c in charts:
                if c.count and c.count > 300:
                    AnomalyDetection.objects.get_or_create(
                        tps=t,
                        url=t.url,
                        message=f"Count: {c.count} higher than 300 - Anomaly Detected",
                        type="Curang"
                    )
                    print(f"Count: {c.count} higher than 300 - Anomaly Detected (Curang)")
                    print(f"TPS: {t.url}")
                if c.count:
                    count += c.count

            if suara_sah and count != suara_sah:
                AnomalyDetection.objects.get_or_create(
                    tps=t,
                    url=t.url,
                    message=f"Count: {count} does not match with Suara Sah: {suara_sah} - Anomaly Detected",
                    type="Human Error"
                )
                print(f"Count: {count} does not match with Suara Sah: {suara_sah} - Anomaly Detected (Human Error)")
                print(f"TPS: {t.url}")

    print("Anomaly Detection Done")


def crawling_kpu(province_code):
    for k in Kelurahan.objects.filter(code__startswith=province_code).all():
        kelurahan = k.code
        kecamatan = kelurahan[:-4]
        kota = kecamatan[:-2]
        provinsi = kota[:-2]

        for tps in range(1, 1000):
            tps = str(tps).zfill(3)
            print(f"Provinsi: {provinsi}, Kota: {kota}, Kecamatan: {kecamatan}, Kelurahan: {kelurahan}, TPS: {tps}")
            response, error = insert_data(provinsi, kota, kecamatan, kelurahan, tps)
            if response:
                if response.status_code == 404:
                    print("TPS NOT FOUND")
                    break
                else:
                    print("Failed to get data from URL")
            else:
                print(error)


def insert_data(provinsi=31, kota=3175, kecamatan=317505, kelurahan=3175051004, tps="073"):
    try:
        url = f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/{provinsi}/{kota}/{kecamatan}/{kelurahan}/{kelurahan}{tps}.json"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json()
            datatps, created = Tps.objects.get_or_create(
                name=f"{kelurahan}{tps}",
                psu=data['psu'],
                ts=data['ts'],
                status_suara=data['status_suara'],
                status_adm=data['status_adm'],
                url=f"https://pemilu2024.kpu.go.id/pilpres/hitung-suara/{provinsi}/{kota}/{kecamatan}/{kelurahan}/{kelurahan}{tps}",
            )

            print(f"TPS: {datatps}, Created: {created}")

            data_chart = data['chart']
            if data_chart:
                for key, value in data_chart.items():
                    Chart.objects.get_or_create(
                        tps=datatps,
                        name=key,
                        count=value
                    )

            data_image = data['images']
            for image in data_image:
                Image.objects.get_or_create(
                    tps=datatps,
                    url=image
                )

            if data.get("administrasi"):
                value = data.get("administrasi")
                Administration.objects.get_or_create(
                    tps=datatps,
                    suara_sah=value.get('suara_sah'),
                    suara_total=value.get('suara_total'),
                    pemilih_dpt_l=value.get('pemilih_dpt_l'),
                    pemilih_dpt_p=value.get('pemilih_dpt_p'),
                    pengguna_dpt_j=value.get('pengguna_dpt_j'),
                    pengguna_dpt_l=value.get('pengguna_dpt_l'),
                    pengguna_dpt_p=value.get('pengguna_dpt_p'),
                    pengguna_dptb_j=value.get('pengguna_dptb_j'),
                    pengguna_dptb_l=value.get('pengguna_dptb_l'),
                    pengguna_dptb_p=value.get('pengguna_dptb_p'),
                    suara_tidak_sah=value.get('suara_tidak_sah'),
                    pengguna_total_j=value.get('pengguna_total_j'),
                    pengguna_total_l=value.get('pengguna_total_l'),
                    pengguna_total_p=value.get('pengguna_total_p'),
                    pengguna_non_dpt_j=value.get('pengguna_non_dpt_j'),
                    pengguna_non_dpt_l=value.get('pengguna_non_dpt_l'),
                    pengguna_non_dpt_p=value.get('pengguna_non_dpt_p')
                )
        return response, None
    except Exception as e:
        return None, e

