from django.http import Http404
from django.shortcuts import render
from django.db.models import Avg, Sum
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import Machine, Cycle, Job, Event
from .serializers import MachineSerializer, JobSerializer, CycleSerializer, EventSerializer
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
import pytz
from django.utils import timezone
from statistics import mean

class StandartResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'num_pages': self.page.number,
            'per_page': self.page.paginator.per_page,
            'result': data,

        })
    
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

    context = {'machine': instance.machine, 'job':instance, 'data_json':data_json}
    
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
            'name': request.data.get('name'),
            'full_job_description': request.data.get('full_job_description')
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

        # Если статус нового задание "Выполняется", значит в предыдущих нужно изменить статус на "Остановлен"
        if data['status'] == 'Выполняется':
            running_jobs = Job.objects.filter(machine__id=data['machine'], status='Выполняется')
            if len(running_jobs) > 0:
                for job in running_jobs:
                    job.status = 'Завершен'
                    job.save()
        
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
        id = request.GET.get("id")
        date_cycle_start = request.GET.get("date_start")
        date_cycle_end = request.GET.get("date_end")
        job = request.GET.get("job")
        page = request.GET.get("page")
        time_ms = request.GET.get("time_ms")

        # Соберем фильтр    
        filter = {}
        if date_cycle_start != None:
            filter['date__gte'] = date_cycle_start
        if date_cycle_end != None:
            filter['date__lt'] = date_cycle_end
        if id != None:
            filter['machine__id'] = id
        if job != None:
            filter['job__uuid_1C'] = job
        if time_ms != None:
            filter['time_ms__gte'] = time_ms

        # Получаем данные
        if len(filter):
            cycles = Cycle.objects.filter(**filter).order_by('date')
        else:
            cycles = Cycle.objects.all().order_by('-date')[:10]
        
        if page != None:
            paginator = StandartResultSetPagination()
            paginator.page_size = 100
            result_page = paginator.paginate_queryset(cycles, request)
            serializer = CycleSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = CycleSerializer(cycles, many=True)
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
        last_50_cycles = Cycle.objects.filter(machine=machine, job=job).order_by('-date')[:50]

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
        deviation1sec_team = 0

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

        cycle_objects = Cycle.objects.filter(machine=machine, job=job, date__gte=date_start)
        if cycle_objects.count() > 0:
            avg_cycle = cycle_objects.aggregate(Avg('time_ms'))
            avg_time_ms = avg_cycle['time_ms__avg']

            countstop_team = len(cycle_objects.filter(time_ms__gt=avg_time_ms*2))
            deviation1sec_team = len(cycle_objects.filter(time_ms__gt=avg_time_ms+1000))

        return {'countstop_team': countstop_team, 'deviation1sec_team': deviation1sec_team}

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
        
        cycle_objects = Cycle.objects.filter(machine=machine, job=job, date__gte=date_start, date__lt=date_stop)
        if cycle_objects.count() > 0:
            avg_cycle = cycle_objects.aggregate(Avg('time_ms'))
            avg_time_ms = avg_cycle['time_ms__avg']
            
            countstop_team = len(cycle_objects.filter(time_ms__gt=avg_time_ms*2))

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
            deviation1sec_team = 0
            countstop_last_team = 0
            socketplan = 0
            socketfact = 0
            timeplan_ms = 0
            
            try:
                # Поиск активного задания
                job_ob = Job.objects.get(machine=machine, status='Выполняется')
                # Найдем последний цикл
                cycle_ob = Cycle.objects.filter(machine=machine, date__gte=date_now - timedelta(hours=0, minutes=5)).order_by('-date')[:1]
                if cycle_ob.count() > 0:
                    date = cycle_ob[0].date.astimezone(tz)
                
                job = job_ob.uuid_1C
                avg_effect_cycle = self.find_avg_50_cycle(machine, job_ob)
                
                stop_team = self.current_team_data(machine, job_ob)
                countstop_team = stop_team['countstop_team']
                deviation1sec_team = stop_team['deviation1sec_team']
                
                countstop_last_team = self.last_team_data(machine, job_ob)

                socketplan = job_ob.socket_plan
                socketfact = job_ob.socket_fact 
                timeplan_ms = int(job_ob.time_plan_ms * 1000)

            except Job.DoesNotExist:
                pass

            machine_info = {'machine_id': machine.id, 
                                    'job_id': job, 
                                    'last_date_cycle': date, 
                                    'avg_effect_cycle': avg_effect_cycle,
                                    'countstop_team': countstop_team,
                                    'deviation1sec_team': deviation1sec_team,
                                    'countstop_last_team': countstop_last_team,
                                    'job_timeplan_ms': timeplan_ms,
                                    'job_socketplan': socketplan,
                                    'job_socketfact': socketfact}

            machines.append(machine_info)

        return JsonResponse(machines, safe=False)
    
class QuantProdApiView(APIView):
    '''Возвращает количество штук, выпущеных по заданию'''
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        date_cycle = request.GET.get("date")
        job = request.GET.get("job")
        cycles = Cycle.objects.filter(machine__id = id, date__gte = date_cycle, job__uuid_1C = job).aggregate(Sum('count'))

        return JsonResponse(cycles, safe=False)
    
class TimeProdApiView(APIView):
    '''Возвращает сумму времени циклов'''
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        date_cycle = request.GET.get("date")
        job = request.GET.get("job")
        cycles = Cycle.objects.filter(machine__id = id, date__gte = date_cycle, job__uuid_1C = job).aggregate(Sum('time_ms'))

        return JsonResponse(cycles, safe=False)
    
class FirstCycleOnDateApiView(APIView):
    '''Возвращает первый цикл'''
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        date_start_cycle = request.GET.get("date_start")
        date_end_cycle = request.GET.get("date_end")
        job = request.GET.get("job")
        cycles = Cycle.objects.filter(machine__id = id, date__gte = date_start_cycle, date__lte = date_end_cycle, job__uuid_1C = job).order_by('date')[:1]

        serializer = CycleSerializer(cycles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LastCycleOnDateApiView(APIView):
    '''Возвращает последний цикл'''
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        date_start_cycle = request.GET.get("date_start")
        date_end_cycle = request.GET.get("date_end")
        job = request.GET.get("job")
        cycles = Cycle.objects.filter(machine__id = id, date__gte = date_start_cycle, date__lte = date_end_cycle, job__uuid_1C = job).order_by('-date')[:1]

        serializer = CycleSerializer(cycles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        