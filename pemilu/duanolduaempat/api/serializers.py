from rest_framework import serializers

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
