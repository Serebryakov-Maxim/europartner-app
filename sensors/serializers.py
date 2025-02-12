from rest_framework import serializers
from .models import WorkArea, Sensor, Parameter, ValueParameter

class ValueParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueParameter
        fields = ['date','sensor','parameter','value']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id','name','work_area']