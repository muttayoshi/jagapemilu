from rest_framework import serializers
from pemilu.duanolduaempat.models import Report


class PercentageSerializer(serializers.Serializer):
    tps_correct = serializers.IntegerField()
    total_suara = serializers.IntegerField()
    anies = serializers.CharField()
    prabowo = serializers.CharField()
    ganjar = serializers.CharField()


class DetailSerializer(serializers.Serializer):
    tps_correct = serializers.IntegerField()
    total_suara = serializers.IntegerField()
    suara_anies = serializers.IntegerField()
    suara_prabowo = serializers.IntegerField()
    suara_ganjar = serializers.IntegerField()
    percentage_anies = serializers.CharField()
    percentage_prabowo = serializers.CharField()
    percentage_ganjar = serializers.CharField()


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["total_suara", "total_tps", "paslon_satu", "paslon_dua", "paslon_tiga"]
        read_only_fields = ["paslon_satu_percentage", "paslon_dua_percentage", "paslon_tiga_percentage"]

        extra_kwargs = {
            "paslon_satu_percentage": {"source": "paslon_satu_percentage"},
            "paslon_dua_percentage": {"source": "paslon_dua_percentage"},
            "paslon_tiga_percentage": {"source": "paslon_tiga_percentage"},
        }
