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
from django.views.decorators.csrf import csrf_exempt,csrf_protect

def history(request):
    """ Формирование произведенных прессформ """
    pressform_list = Pressform.objects.order_by('date_finish', 'assembly')
    years = Pressform.objects.filter(year__gt=0).values('year').annotate(dcount=Count('year')).order_by('year')

    # заполним список с номерами по порядку
    maxcountrow = 10
    table = []
    for year in years:
        list2=[]
        npp = 1
        for cur_pf in pressform_list:
            if cur_pf.year == year['year']:
                d = {'npp':npp, 'name':cur_pf.name, 'type':cur_pf.type}
                list2.append(d)
                npp += 1

        # нужно еще разбить но столбцы, если больше N прессформ в колонке
        new_list = [list2[i:i+maxcountrow] for i in range(0, len(list2), maxcountrow)]
        table.append({'year': year['year'], 'dcount': year['dcount'], 'count_col': len(new_list), 'list_pf':new_list})

    print(years)
    context = {
        'years': years,
        'table': table,
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