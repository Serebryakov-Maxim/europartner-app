from rest_framework import serializers
from .models import Machine, Job, Cycle, Event

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id','name', 'full_job_description']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id','uuid_1C','date','number','name','status','count_plan','time_plan_ms','socket_plan','socket_fact','data_json', 'machine']

class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = ['date','time_ms','machine','job','count','counter']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['date','machine','type','data']