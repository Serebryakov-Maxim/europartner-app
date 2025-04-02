from django.core import serializers
from django.shortcuts import render
from .serializers import ValueParameterSerializer, SensorSerializer
from .models import Sensor, Parameter, WorkArea, ValueParameter
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.utils import timezone


class ValuesSensorApiView(APIView):
    # Get values  
    def get(self, request, *args, **kwargs):
        '''Получение значений'''
        values = ValueParameter.objects.all().order_by('-date')[:10]
        serializer = ValueParameterSerializer(values, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Save values 
    def post(self, request, *args, **kwargs):
        '''Добавление значений'''
        data = {
            'date': datetime.now(),
            'sensor': request.data.get('sensor'),
            'parameter': request.data.get('parameter'),
            'value': request.data.get('value'),
        }

        # find sensor
        try:
            sensor_instance = Sensor.objects.get(name=data['sensor'])
        except Sensor.DoesNotExist:
            sensor_instance = Sensor(name=data['sensor'])
            sensor_instance.save()
        data['sensor'] = sensor_instance.id

        # find parameter
        try:
            parameter_instance = Parameter.objects.get(name=data['parameter'])
        except Parameter.DoesNotExist:
            parameter_instance = Parameter(name=data['parameter'])
            parameter_instance.save()
        data['parameter'] = parameter_instance.id
      
        serializer = ValueParameterSerializer(data=data)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SensorApiView(APIView):
    def get(self, request, *args, **kwargs):
        '''Получение значений'''
        values = Sensor.objects.all()
        serializer = SensorSerializer(values, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListParametersApiView(APIView):
    def get(self, request, *args, **kwargs):
        '''Получение значений для Grafana'''
        sensor = request.GET.get("sensor")
        date_start = request.GET.get("date_start")
        date_end = request.GET.get("date_end")
        parameter = request.GET.get("parameter")

        # Соберем фильтр    
        filter = {}
        if date_start != None:
            filter['date__gte'] = date_start

        if date_end != None:
            filter['date__lt'] = date_end

        if sensor != None:
            try:
                sensor_instance = Sensor.objects.get(name=sensor)
                filter['sensor'] = sensor_instance.id
            except:
                None
            
        if parameter != None:
            try:
                parameter_instance = Parameter.objects.get(name=parameter)
                filter['parameter'] = parameter_instance.id
            except:
                None

        # Получаем данные
        if len(filter):
            values = ValueParameter.objects.filter(**filter).order_by('date').values()
            data = []
            for cur_val in values:
                rec = {}
                rec['date'] = cur_val['date']
                rec['value'] = cur_val['value']
                rec['sensor'] = Sensor.objects.get(pk=cur_val['sensor_id']).name
                rec['parameter'] = Parameter.objects.get(pk=cur_val['parameter_id']).name

                data.append(rec)

            return JsonResponse(data, safe=False)
        else:
            return Response("Empty filter", safe=False)

class ListParameters_v2_ApiView(APIView):
    def get(self, request, *args, **kwargs):
        '''Получение значений для Grafana'''
        sensor = request.GET.get("sensor")
        date_start = request.GET.get("date_start")
        date_end = request.GET.get("date_end")
        parameter = request.GET.get("parameter")

        # Соберем фильтр    
        filter = {}
        if date_start != None:
            filter['date__gte'] = date_start

        if date_end != None:
            filter['date__lt'] = date_end

        if sensor != None:
            try:
                sensor_instance = Sensor.objects.get(name=sensor)
                filter['sensor'] = sensor_instance.id
            except:
                None
            
        if parameter != None:
            try:
                parameter_instance = Parameter.objects.get(name=parameter)
                filter['parameter'] = parameter_instance.id
            except:
                None

        # Получаем данные
        if len(filter):
            values = ValueParameter.objects.filter(**filter).order_by('date')
            data = []
            for i in values:
                data.append({'date':getattr(i, 'date'), 'value':getattr(i, 'value'), 'sensor':i.sensor.name, 'parameter':i.parameter.name})
            print(data)

            return JsonResponse([], safe=False)
        else:
            return Response("Empty filter", safe=False)

class LastParametersApiView(APIView):

    def get(self, request, *args, **kwargs):
        sensor = request.GET.get("sensor")
        parameter = request.GET.get("parameter")

        tz = timezone.get_current_timezone()

                # Соберем фильтр    
        filter = {}

        if sensor != None:
            try:
                sensor_instance = Sensor.objects.get(name=sensor)
                filter['sensor'] = sensor_instance.id
            except:
                None
            
        if parameter != None:
            try:
                parameter_instance = Parameter.objects.get(name=parameter)
                filter['parameter'] = parameter_instance.id
            except:
                None

        # Получаем данные
        if len(filter):
            value = 0
            date = ''
            data = ValueParameter.objects.filter(**filter).order_by('-date')[:1]
            if len(data) > 0:
                value = data[0].value
                date = data[0].date.astimezone(tz)

            return JsonResponse({'date':date,'value': value}, safe=False)
        else:
            return Response("Empty filter", safe=False)
       
