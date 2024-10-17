from django.http import Http404
from django.shortcuts import render, redirect
from django.db.models import Max
from .models import Pressform, TypeWork, Work, Progress, MediaFile
from .forms import PressformForm
from django.db.models import Count
from .serializers import PressformSerializer, PressformLastModifiedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
import json
import requests
from django.views.decorators.csrf import csrf_exempt,csrf_protect

def history(request):
    """ Формирование произведенных прессформ """
    pressform_list = Pressform.objects.filter(year__gt=0).order_by('date_finish', 'assembly')
    years = Pressform.objects.filter(year__gt=0).values('year').annotate(dcount=Count('year')).order_by('year')

    # получим максимальное количество строк
    max_count_str = 0
    for year in years:
        max_count_str = max(max_count_str, year['dcount'])
    max_count_str = int(max_count_str / 2 + 0.5)

    main_table = []
    num_str = 1
    while num_str <= max_count_str:
        for year in years:
            main_table.append({'npp': num_str, 'year':year['year'], 'col': 1, 'name':'', 'type':'', 'id':0})
            main_table.append({'npp': num_str, 'year':year['year'], 'col': 2, 'name':'', 'type':'', 'id':0})
        num_str += 1
    
    # пронумеруем строки по годам
    list_pf = []
    for year in years:
        npp = 1
        t_npp = 1
        for cur_pf in pressform_list:
            if cur_pf.year == year['year']:
                d = {'npp': int(npp / 2 + 0.5), 'year':year['year'], 'name':cur_pf.name, 'type':cur_pf.type, 'col': 2 if (npp % 2 == 0) else 1, 'id': cur_pf.id}
                list_pf.append(d)
                npp += 1

    for str_main_table in main_table:
        for str_list_pf in list_pf:
            if str_main_table['year'] == str_list_pf['year'] and str_main_table['npp'] == str_list_pf['npp'] and str_main_table['col'] == str_list_pf['col']:
                str_main_table['name'] = str_list_pf['name']
                str_main_table['type'] = str_list_pf['type']
                str_main_table['id'] = str_list_pf['id']

    table_new = []
    num_str = 1
    while num_str <= max_count_str:
        list = []
        for str_main_table in main_table:
            if num_str == str_main_table['npp']:
                list.append(str_main_table)
        table_new.append({'num_str': num_str, 'list': list})

        num_str += 1

    context = {
        'years': years,
        'table_new': table_new
    }

    return render(request, 'pressforms/history.html', context)

def media(request):
    """ медиа файлы """
    video_files = MediaFile.objects.filter(type=0).order_by('name')
    foto_files = MediaFile.objects.filter(type=1).order_by('name')
    context = {'video_files': video_files, 'foto_files': foto_files}
    return render(request, 'pressforms/media.html', context)

def pressforms(request):
    """ Формирует список всех прессформ """
    pressforms_list = Pressform.objects.order_by('article')
    context = {'pressforms': pressforms_list}
    return render(request, 'pressforms/pressforms.html', context)

def production(request):
    """ Формирует план производства прессформ """
    pressforms = Pressform.objects.filter(year=0).order_by('assembly')
    count_type = Work.objects.values('type').annotate(dcount=Count('type')).order_by('type')
    typeWorks = TypeWork.objects.order_by('priority')
    works = Work.objects.order_by('priority')
    progress = Progress.objects.all()

    list_progress = []
    for pf in pressforms:
        data = {}
        data['pf'] = pf
        
        list_works = []

        for type in typeWorks:
            for work in works:
                if type != work.type:
                    continue
                data_work = {}
                data_work['work'] = work
                data_work['progress'] = 0
                data_work['week'] = 0
                data_work['week_name'] = ''
                data_work['date_finish'] = ''
                
                for prg in progress:
                    if prg.pressform == pf and prg.work == work:
                        data_work['progress'] = prg.progress
                        data_work['week'] = prg.week

                        if prg.date_finish != None and prg.date_finish > datetime.date(1970, 1, 1):
                            data_work['week_name'] = prg.date_finish.strftime("%d/%m")
                            data_work['date_finish'] = prg.date_finish.strftime("%d.%m.%Y")
                        else:
                            data_work['week_name'] = str(prg.week)
                            data_work['date_finish'] = ''
                     
                        break

                list_works.append(data_work)

        data['list_works'] = list_works
        list_progress.append(data)

    context = {
        'typeWorks': typeWorks,
        'pressforms': pressforms,
        'count_type': count_type,
        'works': works,
        'list_progress': list_progress,
        }

    return render(request, 'pressforms/production.html', context)

def gantt(request):
    '''Диаграмма Ганта'''

    url = 'http://192.168.1.48/ERP/hs/instrumental/projects'
    headers = {'Authorization': "Basic QW5kcm9pZDpYbzdrb25vZg=="}  
    r = requests.get(url, headers=headers)
    data_json = r.json()
    
    series_list = []
    for series in data_json:
        data = []
        for cur_job in series['data']:
            job = {'color': cur_job['color'], 
                   'end': int(cur_job['end']),
                   'isFinish': cur_job['isFinish'], 
                   'name': cur_job['name'],
                   'start': int(cur_job['start']), 
                   'y': cur_job['color']}
            data.append(job)
        project = {'name' : series['name'],
                   'article': series['article'], 
                   'date_start': series['date_start'], 
                   'partner': series['partner'], 
                   'data': data}
        series_list.append(project)

    projects = json.dumps(series_list)

    context = {'projects': projects}
    return render(request, 'pressforms/gantt.html', context)

@csrf_exempt
def operation(request):
    """ Сохраняет введенные данные """
    if request.method == 'POST':
        json_b = request.body
        data_json = json.loads(json_b)
    
        pressform_id = data_json['pressform_id']
        work_id = data_json['work_id']
        oper = data_json['oper']
        week = data_json['week']
        date_finish = data_json['date_finish']
        
        if not date_finish == '':
            parsed_date = datetime.datetime.strptime(date_finish, "%d.%m.%Y").date()
        else:
            parsed_date = datetime.date(1970, 1, 1)

        pressform = Pressform.objects.get(id=int(pressform_id))
        work = Work.objects.get(id=int(work_id))

        prg, created = Progress.objects.update_or_create(pressform = pressform, work = work)
        prg.progress = int(oper)
        try:
            prg.week = int(week)
        except:
            prg.week = 0
        prg.date_finish = parsed_date
        prg.save()

        pressform.save()
    
    return redirect('/pressforms/production/')

def create(request):
    """ Добавление новой прессформы """
    error = ''
    if request.method == 'POST':
        form = PressformForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/pressforms/')
        else:
            error = 'Ошибка заполнения формы'

    form = PressformForm()

    context = {
        'form': form,
        'error': error}
    return render(request, 'pressforms/create.html', context)

def card(request, pressform_id):
    """ Редактирование прессформы """
    try:
        instance = Pressform.objects.get(id=pressform_id)
    except Exception as e:
        raise Http404("Прессформа не найдена!")
        
    error = ''
    if request.method == 'POST':
        form = PressformForm(request.POST or None, instance=instance) 
        if form.is_valid():
            form.save()
            return redirect('/pressforms/')
        else:
            error = 'Ошибка заполнения формы'
    
    form = PressformForm(instance=instance)

    context = {
        'form': form
    }

    return render(request, 'pressforms/create.html', context)

class PressformApiView(APIView):
    # 1. Get events 
    def get(self, request, *args, **kwargs):
        '''Получить список событий'''
        pressforms = Pressform.objects.all().order_by('-date_start')
        serializer = PressformSerializer(pressforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PressformLastModifiedApiView(APIView):
    # 1. Get events 
    def get(self, request, *args, **kwargs):
        '''Получить список событий'''
        pressforms = Pressform.objects.all().order_by('-date_modified')[:1]
        if (pressforms.count() >= 1):
            serializer = PressformLastModifiedSerializer(pressforms[0], many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("", status=status.HTTP_200_OK)