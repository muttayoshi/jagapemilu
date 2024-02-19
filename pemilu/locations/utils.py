import requests
from .models import Kecamatan, Kelurahan, Kota, Provinsi, TingkatSatu, TingkatDua, TingkatTiga, TingkatEmpat


def get_data_from_csv(filename):
    import csv

    with open(f"{filename}.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            code = row[0].split(".")
            if len(code) == 1:
                provinsi, pcreated = Provinsi.objects.get_or_create(name=row[1], code=row[0].replace(".", ""))
                print(f"Provinsi: {provinsi}, Created: {pcreated}")
            elif len(code) == 2:
                provinsi = Provinsi.objects.get(code="".join(code[:-1]))
                city, ccreated = Kota.objects.get_or_create(
                    name=row[1], code=row[0].replace(".", ""), provinsi=provinsi
                )
                print(f"Kota: {city}, Created: {ccreated}")
            elif len(code) == 3:
                city = Kota.objects.get(code="".join(code[:-1]))
                kecamatan, kcreated = Kecamatan.objects.get_or_create(
                    name=row[1], code=row[0].replace(".", ""), kota=city
                )
                print(f"Kecamatan: {kecamatan}, Created: {kcreated}")
            elif len(code) == 4:
                kecamatan = Kecamatan.objects.filter(code="".join(code[:-1])).first()
                kelurahan, klcreated = Kelurahan.objects.get_or_create(
                    name=row[1], code=row[0].replace(".", ""), kecamatan=kecamatan
                )
                print(f"Kelurahan: {kelurahan}, Created: {klcreated}")


def update_data_kelurahan(provinsi_kode, kota_kode, kecamatan_kode, kecamatan_id):
    url = f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi_kode}/{kota_kode}/{kecamatan_kode}.json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    for data in response.json():
        kecamatan = Kecamatan.objects.get(code=kecamatan_kode)
        Kelurahan.objects.update_or_create(
            code=data["kode"],
            # kecamatan=kecamatan_id,
            defaults={"name": data["nama"], "kecamatan": kecamatan},
        )


def update_data_kecamatan(provinsi_kode, kota_kode, kota_id):
    url = f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi_kode}/{kota_kode}.json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    for kec in response.json():
        kota = Kota.objects.get(code=kota_kode)
        kecamatan, created = Kecamatan.objects.update_or_create(
            code=kec["kode"],
            # kota=kota_id,
            defaults={"name": kec["nama"], "kota": kota},
        )
        print(f"{created}, {kecamatan.id} {kecamatan.name} {kec['kode']}")
        update_data_kelurahan(provinsi_kode, kota_kode, kec["kode"], kecamatan.id)


def update_data_kota(provinsi_kode, provinsi_id):
    url = f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi_kode}.json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    for city in response.json():
        provinsi = Provinsi.objects.get(code=provinsi_kode)
        kota, created = Kota.objects.update_or_create(
            code=city["kode"],
            # provinsi=provinsi_id,
            defaults={"name": city["nama"], "provinsi": provinsi},
        )
        print(f"{created}, {kota.id} {kota.name} {city['kode']}")
        update_data_kecamatan(provinsi_kode, city["kode"], kota.id)


def update_data_province():
    url = "https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/0.json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    for prov in response.json():
        provinsi, created = Provinsi.objects.update_or_create(
            code=prov["kode"],
            defaults={"name": prov["nama"]},
        )
        print(f"{created}, {provinsi.id} {provinsi.name} {prov['kode']}")
        update_data_kota(prov["kode"], provinsi.id)


def update_data_luar_negeri_tingkat_satu():
    TingkatSatu.objects.update_or_create(
        code="99",
        defaults={"name": "LUAR NEGERI"},
    )

    update_data_luar_negeri_tingkat_dua("99")

def update_data_luar_negeri_tingkat_dua(satu_code):
    url = f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{satu_code}.json"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    for dua in response.json():
        TingkatDua.objects.update_or_create(
            code=dua["kode"],
            defaults={"name": dua["nama"], "tingkat_satu": TingkatSatu.objects.get(code=satu_code)},
        )
        update_data_luar_negeri_tingkat_tiga(satu_code, dua["kode"])


def update_data_luar_negeri_tingkat_tiga(satu_code, dua_code):
    url = f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{satu_code}/{dua_code}.json"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    for tiga in response.json():
        TingkatTiga.objects.update_or_create(
            code=tiga["kode"],
            defaults={"name": tiga["nama"], "tingkat_dua": TingkatDua.objects.get(code=dua_code)},
        )
        update_data_luar_negeri_tingkat_empat(satu_code, dua_code, tiga["kode"])


def update_data_luar_negeri_tingkat_empat(satu_code, dua_code, tiga_code):
    url = f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{satu_code}/{dua_code}/{tiga_code}.json"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    for empat in response.json():
        TingkatEmpat.objects.update_or_create(
            code=empat["kode"],
            defaults={"name": empat["nama"], "tingkat_tiga": TingkatTiga.objects.get(code=tiga_code)},
        )
