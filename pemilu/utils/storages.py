import boto3
import requests
import tempfile
import datetime

from config.settings.base import env

from pemilu.duanolduaempat.models import Image, BackupCHasil


class S3Storage:
    def __init__(self):
        self.bucket_name = env("CONTABO_S3_BUCKET_NAME")
        self.s3 = boto3.client('s3', endpoint_url=env("CONTABO_S3_ENDPOINT_URL"),
                                 aws_access_key_id=env("CONTABO_S3_ACCESS_KEY_ID"),
                                 aws_secret_access_key=env("CONTABO_S3_SECRET_ACCESS_KEY")
                               )
        self.session = boto3.Session()

    def backup_image(self, image_id):
        image = Image.objects.get(id=image_id, is_backup=False)
        if image and image.url:
            backup = BackupCHasil.objects.filter(kpu_url=image.url).first()
            if not backup:
                image_url = image.url
                r = requests.get(image_url, stream=True)
                if r.status_code == 200:
                    filename = f"{image.tps.name}-{datetime.datetime.now().isoformat()}.jpg"
                    self.s3.put_object(Body=r.content, Bucket=self.bucket_name, Key=filename)
                    public_url = f"https://eu2.contabostorage.com/3e6fed6b6c9b4ce8bb143ddd4481477e:{self.bucket_name}/{filename}"
                    BackupCHasil.objects.create(img=image, kpu_url=image.url, filename=filename, s3_url=public_url)
                    return filename
            else:
                image.is_backup = True
                image.save()
