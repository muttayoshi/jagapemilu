from django.db import models
from model_utils.models import TimeStampedModel


class Tps(TimeStampedModel):
    name = models.CharField(max_length=100)
    psu = models.CharField(null=True, blank=True)
    ts = models.DateTimeField(null=True, blank=True)
    status_suara = models.BooleanField(default=False)
    status_adm = models.BooleanField(default=False)
    url = models.URLField(null=True, blank=True)
    has_anomaly = models.BooleanField(default=False)
    province = models.ForeignKey(
        "locations.Provinsi", on_delete=models.CASCADE, related_name="tps", null=True, blank=True
    )

    def __str__(self):
        from pemilu.locations.models import Kelurahan

        kelurahan = Kelurahan.objects.filter(code=self.name[:-3]).first()
        if kelurahan and kelurahan.kecamatan and kelurahan.kecamatan.kota and kelurahan.kecamatan.kota.provinsi:
            return (
                f"{kelurahan.kecamatan.kota.provinsi.name} - {kelurahan.kecamatan.kota.name} - "
                f"{kelurahan.kecamatan.name} - {kelurahan.name} | TPS: {self.name[-3:]}"
            )
        else:
            return self.name

    class Meta:
        ordering = ("-created",)


class Chart(TimeStampedModel):
    tps = models.ForeignKey(Tps, on_delete=models.CASCADE, related_name="charts")
    name = models.CharField(max_length=100)
    count = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.count}"

    class Meta:
        ordering = ("-created",)


class Image(TimeStampedModel):
    tps = models.ForeignKey(Tps, on_delete=models.CASCADE, related_name="images")
    url = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    # def __str__(self):
    #     return self.url

    class Meta:
        ordering = ("-created",)


class Administration(TimeStampedModel):
    tps = models.ForeignKey(Tps, on_delete=models.CASCADE, related_name="administrations")
    suara_sah = models.IntegerField(null=True, blank=True)
    suara_total = models.IntegerField(null=True, blank=True)
    pemilih_dpt_l = models.IntegerField(null=True, blank=True)
    pemilih_dpt_p = models.IntegerField(null=True, blank=True)
    pengguna_dpt_j = models.IntegerField(null=True, blank=True)
    pengguna_dpt_l = models.IntegerField(null=True, blank=True)
    pengguna_dpt_p = models.IntegerField(null=True, blank=True)
    pengguna_dptb_j = models.IntegerField(null=True, blank=True)
    pengguna_dptb_l = models.IntegerField(null=True, blank=True)
    pengguna_dptb_p = models.IntegerField(null=True, blank=True)
    suara_tidak_sah = models.IntegerField(null=True, blank=True)
    pengguna_total_j = models.IntegerField(null=True, blank=True)
    pengguna_total_l = models.IntegerField(null=True, blank=True)
    pengguna_total_p = models.IntegerField(null=True, blank=True)
    pengguna_non_dpt_j = models.IntegerField(null=True, blank=True)
    pengguna_non_dpt_l = models.IntegerField(null=True, blank=True)
    pengguna_non_dpt_p = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.suara_sah} - {self.suara_total}"

    class Meta:
        ordering = ("-created",)


class AnomalyDetection(TimeStampedModel):
    tps = models.ForeignKey(Tps, on_delete=models.CASCADE, related_name="anomalies")
    url = models.URLField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    is_reported = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.url}"

    class Meta:
        ordering = ("-created",)


class Report(TimeStampedModel):
    name = models.CharField(max_length=100)
    total_suara = models.IntegerField(null=True, blank=True)
    total_tps = models.IntegerField(null=True, blank=True)
    paslon_satu = models.IntegerField(null=True, blank=True)
    paslon_dua = models.IntegerField(null=True, blank=True)
    paslon_tiga = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.total_suara}"

    class Meta:
        ordering = ("-created",)


class ReportDetail(TimeStampedModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="details")
    province = models.ForeignKey(
        "locations.Provinsi", on_delete=models.CASCADE, related_name="reports", null=True, blank=True
    )
    total_suara = models.IntegerField(null=True, blank=True)
    total_tps = models.IntegerField(null=True, blank=True)
    paslon_satu = models.IntegerField(null=True, blank=True)
    paslon_dua = models.IntegerField(null=True, blank=True)
    paslon_tiga = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.total_suara}"

    class Meta:
        ordering = ("-created",)
