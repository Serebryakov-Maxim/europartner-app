from rest_framework import serializers
from .models import Machine, Job

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id','name']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id','uuid_1C','date','number','name','status','count_plan','time_plan_ms','socket_plan','socket_fact','data_json', 'machine']