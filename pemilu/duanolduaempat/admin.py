from django.contrib import admin

from .models import Administration, AnomalyDetection, Chart, Image, Tps


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
    list_filter = ("status_suara", "status_adm", "has_anomaly")
    search_fields = ("name", "psu", "ts", "url")
    list_per_page = 25
    inlines = [ChartInline, ImageInline, AdministrationInline]


@admin.register(AnomalyDetection)
class AnomalyDetectionAdmin(admin.ModelAdmin):
    list_display = ("tps", "message")
    list_filter = ("type",)
    search_fields = ("tps", "message")
    list_per_page = 25
