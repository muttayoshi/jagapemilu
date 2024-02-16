from django.contrib import admin

from .models import Kecamatan, Kelurahan, Kota, Provinsi


@admin.register(Provinsi)
class ProvinsiAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created", "modified")
    search_fields = ("name", "code")
    list_filter = ("created", "modified")


@admin.register(Kota)
class KotaAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "provinsi", "created", "modified")
    search_fields = ("name", "code", "provinsi")
    list_filter = ("created", "modified")


@admin.register(Kecamatan)
class KecamatanAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "kota", "created", "modified")
    search_fields = ("name", "code", "kota")
    list_filter = ("created", "modified")


@admin.register(Kelurahan)
class KelurahanAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "kecamatan", "created", "modified")
    search_fields = ("name", "code", "kecamatan")
    list_filter = ("created", "modified")
