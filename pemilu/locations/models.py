from django.db import models
from model_utils.models import TimeStampedModel


class Provinsi(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)
        verbose_name_plural = "Provinsi"


class Kota(TimeStampedModel):
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE, related_name="kota")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)
        verbose_name_plural = "Kota"


class Kecamatan(TimeStampedModel):
    kota = models.ForeignKey(Kota, on_delete=models.CASCADE, related_name="kecamatan")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)
        verbose_name_plural = "Kecamatan"


class Kelurahan(TimeStampedModel):
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE, related_name="kelurahan", null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("created",)
        verbose_name_plural = "Kelurahan"


class TingkatSatu(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class TingkatDua(TimeStampedModel):
    tingkat_satu = models.ForeignKey(TingkatSatu, on_delete=models.CASCADE, related_name="tingkat_dua")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class TingkatTiga(TimeStampedModel):
    tingkat_dua = models.ForeignKey(TingkatDua, on_delete=models.CASCADE, related_name="tingkat_tiga")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class TingkatEmpat(TimeStampedModel):
    tingkat_tiga = models.ForeignKey(TingkatTiga, on_delete=models.CASCADE, related_name="tingkat_empat")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)
