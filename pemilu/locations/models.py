from django.db import models
from model_utils.models import TimeStampedModel


class Provinsi(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class Kota(TimeStampedModel):
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE, related_name="kota")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class Kecamatan(TimeStampedModel):
    kota = models.ForeignKey(Kota, on_delete=models.CASCADE, related_name="kecamatan")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class Kelurahan(TimeStampedModel):
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE, related_name="kelurahan", null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("created",)
