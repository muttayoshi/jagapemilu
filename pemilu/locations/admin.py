from django.contrib import admin

from .models import Kecamatan, Kelurahan, Kota, Provinsi, TingkatDua, TingkatEmpat, TingkatSatu, TingkatTiga


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


# @admin.register(TingkatSatu)
# class TingkatSatuAdmin(admin.ModelAdmin):
#     list_display = ("name", "code", "created", "modified")
#     search_fields = ("name", "code")
#     list_filter = ("created", "modified")


# @admin.register(TingkatDua)
# class TingkatDuaAdmin(admin.ModelAdmin):
#     list_display = ("name", "code", "tingkat_satu", "created", "modified")
#     search_fields = ("name", "code", "tingkat_satu")
#     list_filter = ("created", "modified")


# @admin.register(TingkatTiga)
# class TingkatTigaAdmin(admin.ModelAdmin):
#     list_display = ("name", "code", "tingkat_dua", "created", "modified")
#     search_fields = ("name", "code", "tingkat_dua")
#     list_filter = ("created", "modified")


# @admin.register(TingkatEmpat)
# class TingkatEmpatAdmin(admin.ModelAdmin):
#     list_display = ("name", "code", "tingkat_tiga", "created", "modified")
#     search_fields = ("name", "code", "tingkat_tiga")
#     list_filter = ("created", "modified")
