from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Machine, Cycle, Job, Event
from .serializers import MachineSerializer, JobSerializer, CycleSerializer, EventSerializer
import json

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

    context = {'machine':instance}
    return render(request, 'tpa/machine.html', context)

def machine_last_data(request, machine_id):
    """ Просмотр последних данных с контроллера """
    try:
        instance = Machine.objects.get(id=machine_id)
    except Exception as e:
        raise Http404("Станок не найдена!")

    cycles = Cycle.objects.filter(machine_id=machine_id).order_by('-date')[:10]
    events = Event.objects.filter(machine_id=machine_id).order_by('-date')[:10]

    context = {'machine':instance, 'cycles': cycles, 'events': events}
    return render(request, 'tpa/last_data.html', context)

def machine_job(request, machine_id):
    """ Просмотр задания """
    try:
        instance = Job.objects.get(machine_id=machine_id, status='Выполняется')
    except Exception as e:
        machine = Machine.objects.get(id=machine_id)
        context = {'name': machine.name, 'number': machine.id}
        return render(request, 'tpa/job_empty.html', context)
    
    data_str = instance.data_json
    data_json = json.loads(data_str)

    context = {'job':instance, 'data_json':data_json}

    return render(request, 'tpa/job.html', context)

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
        
    def get_machine(self, id):
        '''Метод возвращает станок по id'''
        try:
            return Machine.objects.get(id=id)
        except Machine.DoesNotExist:
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
            'uuid_1C':request.data.get('uuid_1C'), 
            'date': request.data.get('date'),
            'number': request.data.get('number'),
            'name': request.data.get('name'),
            'status': request.data.get('status'),
            'count_plan': request.data.get('count_plan'),
            'time_plan_ms': request.data.get('time_plan_ms'),
            'socket_plan': request.data.get('socket_plan'),
            'socket_fact': request.data.get('socket_fact'),
            'data_json': request.data.get('data_json'),
            'machine': request.data.get('machine')
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

class CycleApiView(APIView):
    # 1. Get cycles  
    def get(self, request, *args, **kwargs):
        '''Получить список цикло'''
        machines = Cycle.objects.all().order_by('-date')[:10]
        serializer = CycleSerializer(machines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     # 2. Create / update
    def post(self, request, *args, **kwargs):
        '''Создание циклов'''
        data = {
            'date': request.data.get('date'),
            'time_ms': request.data.get('time_ms'),
            'job': request.data.get('job'),
            'count': request.data.get('count'),
            'counter': request.data.get('counter'),
            'machine': request.data.get('machine')
        }
        # find job
        try:
            job_instance = Job.objects.get(machine_id=data['machine'], status='Выполняется')
        except:
            job_instance = Job.objects.get(uuid_1C='00000000-0000-0000-0000-000000000000')
        data['job'] = job_instance.id
        # find count
        if job_instance.socket_fact > 0:
            data['count'] = job_instance.socket_fact
        else:
            data['count'] = job_instance.socket_plan
        
        serializer = CycleSerializer(data=data)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventApiView(APIView):
    # 1. Get events 
    def get(self, request, *args, **kwargs):
        '''Получить список событий'''
        machines = Event.objects.all().order_by('-date')[:10]
        serializer = EventSerializer(machines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     # 2. Create / update
    def post(self, request, *args, **kwargs):
        '''Создание событий'''
        data = {
            'date': request.data.get('date'),
            'machine': request.data.get('machine'),
            'type': request.data.get('type'),
            'data': request.data.get('data')
        }
        
        serializer = EventSerializer(data=data)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)