from django.http import Http404
from django.shortcuts import render
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Machine, Cycle, Job, Event
from .serializers import MachineSerializer, JobSerializer, CycleSerializer, EventSerializer
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
import pytz
from django.utils import timezone
from statistics import mean

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
    tz = timezone.get_current_timezone()
    date_now = datetime.now().astimezone(tz)
    date_start = (date_now - timedelta(days=1))
    try:
        instance = Machine.objects.get(id=machine_id)
    except Exception as e:
        raise Http404("Станок не найдена!")

    cycles = Cycle.objects.filter(machine_id=machine_id, date__gte=date_start).order_by('-date')[:10]
    events = Event.objects.filter(machine_id=machine_id, date__gte=date_start).order_by('-date')[:10]

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
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
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
        '''Получить список циклов'''
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

class EffectCycleApiView(APIView):

    def find_avg_50_cycle(self, machine, job):
        avg_effect_time_ms = 0
        # соберем последние 50 циклов
        last_50_cycles = Cycle.objects.filter(machine_id=machine, job=job).order_by('-date')[:50]

        if last_50_cycles.count() > 0:
            # циклы есть, возьмем средний показатель времени
            avg_cycle = last_50_cycles.aggregate(Avg('time_ms'))
            avg_time_ms = avg_cycle['time_ms__avg']

            # найдем еффективное время цикла, всё что меньше среднего + 1 сек.
            list_time_ms = []
            for el in last_50_cycles:
                if el.time_ms < avg_time_ms*2:
                    list_time_ms.append(el.time_ms)

            avg_effect_time_ms = mean(list_time_ms)

        return avg_effect_time_ms
      
    def current_team_data(self, machine, job):
        tz = timezone.get_current_timezone()
        date_now = datetime.now().astimezone(tz)
        countstop_team = 0

        if date_now.hour >= 8 and date_now.hour < 20:
            # дневная смена
            date_start = date_now.replace(hour=8, minute=0, second=0)
        elif date_now.hour >= 20:
            # ночная смена сегодня
            date_start = date_now.replace(hour=20, minute=0, second=0)
        elif date_now.hour < 8:
            # ночная смена сегодня
            date_start = (date_now - timedelta(days=1)).replace(hour=20, minute=0, second=0)
        else:
            pass

        cycle_objects = Cycle.objects.filter(machine_id=machine, job=job, date__gte=date_start)
        if cycle_objects.count() > 0:
            avg_cycle = cycle_objects.aggregate(Avg('time_ms'))
            avg_time_ms = avg_cycle['time_ms__avg']

            list_time_ms = []
            for el in cycle_objects:
                if el.time_ms > avg_time_ms*2:
                    list_time_ms.append(el.time_ms)

            countstop_team = len(list_time_ms)

        return countstop_team

    def last_team_data(self, machine, job):
        tz = timezone.get_current_timezone()
        date_now = datetime.now().astimezone(tz)
        countstop_team = 0

        if date_now.hour >= 8 and date_now.hour < 20:
            # сейчас дневная смена, значит прошлая началась вчера
            date_start = (date_now - timedelta(days=1)).replace(hour=20, minute=0, second=0)
            date_stop = date_now.replace(hour=8, minute=0, second=0)

        elif date_now.hour >= 20:
            # ночная смена сегодня, значит прошлая сегодня с 8-ми
            date_start = date_now.replace(hour=8, minute=0, second=0)
            date_stop = date_now.replace(hour=20, minute=0, second=0)
        elif date_now.hour < 8:
            # ночная смена сегодня, значит прошлая началась вчера с 8-20
            date_start = (date_now - timedelta(days=1)).replace(hour=8, minute=0, second=0)
            date_stop = (date_now - timedelta(days=1)).replace(hour=20, minute=0, second=0)
        else:
            pass
        
        cycle_objects = Cycle.objects.filter(machine_id=machine, job=job, date__gte=date_start, date__lt=date_stop)
        if cycle_objects.count() > 0:
            avg_cycle = cycle_objects.aggregate(Avg('time_ms'))
            avg_time_ms = avg_cycle['time_ms__avg']

            list_time_ms = []
            for el in cycle_objects:
                if el.time_ms > avg_time_ms*2:
                    list_time_ms.append(el.time_ms)

            countstop_team = len(list_time_ms)

        return countstop_team

    def get(self, request, *args, **kwargs):
        tz = timezone.get_current_timezone()
        date_now = datetime.now().astimezone(tz)
        machines = []
        machines_list = Machine.objects.order_by('id')
        avg_cycle = 0

        for machine in machines_list:
            job = ''
            date = ''
            avg_effect_cycle = 0
            countstop_team = 0
            countstop_last_team = 0
            
            try:
                # Поиск активного задания
                job_ob = Job.objects.get(machine_id=machine.id, status='Выполняется')
                # Найдем последний цикл
                cycle_ob = Cycle.objects.filter(machine_id=machine.id, job=job_ob, date__gte=date_now - timedelta(hours=0, minutes=5)).order_by('-date')[:1]
                if cycle_ob.count() > 0:
                    date = cycle_ob[0].date.astimezone(tz)
                
                job = job_ob.uuid_1C
                avg_effect_cycle = self.find_avg_50_cycle(machine.id, job_ob)
                #countstop_team = self.current_team_data(machine.id, job_ob)
                #countstop_last_team = self.last_team_data(machine.id, job_ob)

            except Job.DoesNotExist:
                pass

            machine_info = {'id': machine.id, 
                                    'job': job, 
                                    'last_date_cycle': date, 
                                    'avg_effect_cycle': avg_effect_cycle,
                                    'countstop_team': countstop_team,
                                    'countstop_last_team': countstop_last_team,}

            machines.append(machine_info)

        return JsonResponse(machines, safe=False)