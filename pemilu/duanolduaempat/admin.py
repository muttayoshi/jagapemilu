from django.contrib import admin

from .models import Administration, AnomalyDetection, Chart, Image, Report, ReportDetail, Tps


class ChartInline(admin.TabularInline):
    model = Chart
    extra = 0
    fieldsets = [
        (None, {"fields": ["name", "count"]}),
    ]
    ordering = ("name",)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    ordering = ("-created",)


class AdministrationInline(admin.TabularInline):
    model = Administration
    extra = 0
    ordering = ("-created",)


@admin.register(Tps)
class TpsAdmin(admin.ModelAdmin):
    list_display = ("name", "has_anomaly", "psu", "ts", "status_suara", "status_adm", "url")
    list_filter = ("status_suara", "status_adm", "has_anomaly", "province")
    search_fields = ("name", "psu", "ts", "url")
    list_per_page = 25
    inlines = [ChartInline, ImageInline, AdministrationInline]


@admin.register(AnomalyDetection)
class AnomalyDetectionAdmin(admin.ModelAdmin):
    list_display = ("tps", "message")
    list_filter = ("type",)
    search_fields = ("tps", "message")
    list_per_page = 25


class ReportDetailInline(admin.TabularInline):
    model = ReportDetail
    list_display = ("province", "total_suara", "total_tps", "paslon_satu", "paslon_dua", "paslon_tiga")
    extra = 0
    ordering = ("-created",)
    # readonly_fields = ("paslon_satu_percentage", "paslon_dua_percentage", "paslon_tiga_percentage")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("total_suara", "total_tps", "paslon_satu", "paslon_dua", "paslon_tiga", "paslon_satu_percentage", "paslon_dua_percentage", "paslon_tiga_percentage")

    list_per_page = 25
    inlines = [ReportDetailInline]
    readonly_fields = ("paslon_satu_percentage", "paslon_dua_percentage", "paslon_tiga_percentage")
