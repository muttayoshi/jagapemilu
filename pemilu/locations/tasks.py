import requests

from config import celery_app
from pemilu.locations.models import Provinsi
from pemilu.locations.utils import update_data_kota, update_data_province


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def update_province():
    update_data_province()
    return "update_province"


@celery_app.task(soft_time_limit=60 * 60 * 24, time_limit=60 * 60 * 24)
def upsert_province(prov):
    provinsi, created = Provinsi.objects.update_or_create(
        code=prov["kode"],
        defaults={"name": prov["nama"]},
    )
    print(f"{created}, {provinsi.id} {provinsi.name} {prov['kode']}")
    update_data_kota(prov["kode"], provinsi.id)


def get_data_location_for_kpu():
    from pemilu.duanolduaempat.utils import divide_data

    url = "https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/0.json"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    data_province = response.json()

    total_data = len(data_province)
    num_parts = 3
    id_ranges = divide_data(total_data, num_parts)

    divided_data = []
    for id_range in id_ranges:
        # Get the start and end indices
        start, end = id_range

        # Slice the data_province list using the start and end indices
        # Python list slicing is zero-indexed and the end index is exclusive
        # We subtract 1 from start and end to get the correct slices
        chunk = data_province[start - 1 : end]

        # Append the chunk to the divided_data list
        divided_data.append(chunk)

    for province_list in divided_data:
        for _p in province_list:
            upsert_province.delay(_p)
