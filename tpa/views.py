from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Machine, Cycle, Job
from .serializers import MachineSerializer, JobSerializer

def list(request):
    machines_list = Machine.objects.order_by('id')
    context = {'machines': machines_list}
    return render(request, 'tpa/list.html', context)


def machine_card(request, machine_id):
    """ Просмотр карточки станка """
    try:
        instance = Machine.objects.get(id=machine_id)
    except Exception as e:
        raise Http404("Станок не найдена!")

    cycles = Cycle.objects.filter(machine_id=machine_id).order_by('-date')[:10]

    context = {'machine':instance, 'cycles': cycles}
    return render(request, 'tpa/machine.html', context)


class MachineListApiView(APIView):

    def get_object(self, id):
        '''Метод возвращает станок по id'''
        try:
            return Machine.objects.get(id=id)
        except Machine.DoesNotExist:
            return None

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''Получить список станков'''
        machines = Machine.objects.all()
        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
     # 2. Create / update
    def post(self, request, *args, **kwargs):
        '''Создание/обновление станков'''
        data = {
            'id': request.data.get('id'), 
            'name': request.data.get('name')
        }
        
        machine_instance = self.get_object(data['id'])
        if not machine_instance:
            serializer = MachineSerializer(data=data)
        else:
            serializer = MachineSerializer(instance = machine_instance, data=data, partial = True)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JobListApiView(APIView):
    
    def get_object(self, id):
        '''Метод возвращает задание по id'''
        try:
            return Job.objects.get(id=id)
        except Job.DoesNotExist:
            return None
        
    def get_object_by_uuid(self, uuid_1C):
        '''Метод возвращает задание по uuid'''
        try:
            return Job.objects.get(uuid_1C=uuid_1C)
        except Job.DoesNotExist:
            return None
        
    # 1. List all
    def get(self, request, *args, **kwargs):
        '''Получить список заданий'''
        machines = Job.objects.all()
        serializer = JobSerializer(machines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     # 2. Create / update
    def post(self, request, *args, **kwargs):
        '''Создание/обновление заданий'''
        data = {
            'uuid_1C': request.data.get('uuid_1C'), 
            'date': request.data.get('date'),
            'number': request.data.get('number'),
            'name': request.data.get('name'),
            'status': request.data.get('status'),
            'count_plan': request.data.get('count_plan'),
            'time_plan_ms': request.data.get('time_plan_ms'),
            'socket_plan': request.data.get('socket_plan'),
            'socket_fact': request.data.get('socket_fact'),
            'data_json': request.data.get('data_json')
        }
        
        job_instance = self.get_object_by_uuid(data['uuid_1C'])
        if not job_instance:
            serializer = JobSerializer(data=data)
        else:
            serializer = JobSerializer(instance = job_instance, data=data, partial = True)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)