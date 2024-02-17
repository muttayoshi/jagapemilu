from rest_framework import serializers
from pemilu.duanolduaempat.models import Report, ReportDetail


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


class ReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDetail
        fields = ["total_suara", "total_tps", "paslon_satu", "paslon_dua", "paslon_tiga"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.total_suara and instance.paslon_satu and instance.paslon_dua and instance.paslon_tiga:
            data["paslon_satu_percentage"] = f"{(instance.paslon_satu / instance.total_suara) * 100} %"
            data["paslon_dua_percentage"] = f"{(instance.paslon_dua / instance.total_suara) * 100} %"
            data["paslon_tiga_percentage"] = f"{(instance.paslon_tiga / instance.total_suara) * 100} %"
        else:
            data["paslon_satu_percentage"] = "0 %"
            data["paslon_dua_percentage"] = "0 %"
            data["paslon_tiga_percentage"] = "0 %"
        data["province"] = instance.province.name
        data["province_code"] = instance.province.code

        return data


class ReportSerializer(serializers.ModelSerializer):
    details = ReportDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Report
        fields = ["total_suara", "total_tps", "paslon_satu", "paslon_dua", "paslon_tiga", "details"]

        extra_kwargs = {
            "paslon_satu_percentage": {"source": "paslon_satu_percentage"},
            "paslon_dua_percentage": {"source": "paslon_dua_percentage"},
            "paslon_tiga_percentage": {"source": "paslon_tiga_percentage"},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.total_suara and instance.paslon_satu and instance.paslon_dua and instance.paslon_tiga:
            data["paslon_satu_percentage"] = f"{(instance.paslon_satu / instance.total_suara) * 100} %"
            data["paslon_dua_percentage"] = f"{(instance.paslon_dua / instance.total_suara) * 100} %"
            data["paslon_tiga_percentage"] = f"{(instance.paslon_tiga / instance.total_suara) * 100} %"
        else:
            data["paslon_satu_percentage"] = "0 %"
            data["paslon_dua_percentage"] = "0 %"
            data["paslon_tiga_percentage"] = "0 %"
        return data
