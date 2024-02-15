import requests
import json

from pemilu.locations.models import Provinsi, Kota, Kecamatan, Kelurahan
from pemilu.duanolduaempat.models import Tps, Chart, Image, Administration

def crawling_kpu():

    kelurahan = Kelurahan.objects.all()

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

                    data_administration = data['administration']

                    for key, value in data_administration.items():
                        if data_administration:
                            Administration.objects.get_or_create(
                                tps=datatps,
                                suara_sah=value['suara_sah'],
                                suara_total=value['suara_total'],
                                pemilih_dpt_l=value['pemilih_dpt_l'],
                                pemilih_dpt_p=value['pemilih_dpt_p'],
                                pengguna_dpt_j=value['pengguna_dpt_j'],
                                pengguna_dpt_l=value['pengguna_dpt_l'],
                                pengguna_dpt_p=value['pengguna_dpt_p'],
                                pengguna_dptb_j=value['pengguna_dptb_j'],
                                pengguna_dptb_l=value['pengguna_dptb_l'],
                                pengguna_dptb_p=value['pengguna_dptb_p'],
                                suara_tidak_sah=value['suara_tidak_sah'],
                                pengguna_total_j=value['pengguna_total_j'],
                                pengguna_total_l=value['pengguna_total_l'],
                                pengguna_total_p=value['pengguna_total_p'],
                                pengguna_non_dpt_j=value['pengguna_non_dpt_j'],
                                pengguna_non_dpt_l=value['pengguna_non_dpt_l'],
                                pengguna_non_dpt_p=value['pengguna_non_dpt_p']
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
