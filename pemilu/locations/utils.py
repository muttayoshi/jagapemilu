from .models import Kecamatan, Kelurahan, Kota, Provinsi


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
