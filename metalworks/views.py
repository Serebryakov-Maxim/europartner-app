from django.http import Http404
from django.shortcuts import render, redirect
from .models import mw_Detail, mw_Progress, mw_Work, Partner
from django.views import View
from .forms import DetailForm
from django.db.models import Count
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DetailSerializer, DetailLastModifiedSerializer
import json
from django.views.decorators.csrf import csrf_exempt,csrf_protect

def details(request):
    """ Формирует список всех прессформ """
    details_list = mw_Detail.objects.order_by('article')
    context = {'details': details_list}
    return render(request, 'metalworks/details.html', context)

def history(request):
    """ Формирует список выполненных деталей """
    detail_list = mw_Detail.objects.filter(year__gt=0).order_by('date_finish', 'assembly')
    years = mw_Detail.objects.filter(year__gt=0).values('year').annotate(dcount=Count('year')).order_by('year')

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
        for cur_pf in detail_list:
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

    return render(request, 'metalworks/history.html', context)

def production(request):
    """ Формирует список деталей в производстве """
    details = mw_Detail.objects.filter(year=0).order_by('assembly')
    works = mw_Work.objects.order_by('priority')
    progress = mw_Progress.objects.all()

    list_progress = []
    for dt in details:
        data = {}
        data['dt'] = dt
        
        list_works = []
        
        for work in works:
            data_work = {}
            data_work['work'] = work
            data_work['progress'] = 0
            data_work['week'] = 0
            data_work['week_name'] = ''
            data_work['date_finish'] = ''
            
            try:
                prg = progress.get(detail=dt, work=work)
                data_work['progress'] = prg.progress
                data_work['week'] = prg.week

                if prg.date_finish != None and prg.date_finish > datetime.date(1970, 1, 1):
                    data_work['week_name'] = prg.date_finish.strftime("%d/%m")
                    data_work['date_finish'] = prg.date_finish.strftime("%d.%m.%Y")
                else:
                    data_work['week_name'] = str(prg.week)
                    data_work['date_finish'] = ''
            except mw_Progress.DoesNotExist:
                pass

            list_works.append(data_work)

        data['list_works'] = list_works
        list_progress.append(data)

    context = {
        'details': details,
        'works': works,
        'list_progress': list_progress,
        }

    return render(request, 'metalworks/production.html', context)

def create(request):
    """ Добавление новой детали """
    error = ''
    if request.method == 'POST':
        form = DetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/metalworks/')
        else:
            error = 'Ошибка заполнения формы'

    form = DetailForm()

    context = {
        'form': form,
        'error': error}
    return render(request, 'metalworks/create.html', context)

def card(request, detail_id):
    """ Редактирование детали """
    try:
        instance = mw_Detail.objects.get(id=detail_id)
    except Exception as e:
        raise Http404("Деталь не найдена!")
        
    error = ''
    if request.method == 'POST':
        form = DetailForm(request.POST or None, instance=instance) 
        if form.is_valid():
            form.save()
            return redirect('/metalworks/')
        else:
            error = 'Ошибка заполнения формы'
    
    form = DetailForm(instance=instance)

    context = {
        'form': form,
        'error': error
    }

    return render(request, 'metalworks/create.html', context)

@csrf_exempt
def operation(request):
    """ Сохраняет введенные данные """
    if request.method == 'POST':
        json_b = request.body
        data_json = json.loads(json_b)
    
        detail_id = data_json['pressform_id']
        work_id = data_json['work_id']
        oper = data_json['oper']
        week = data_json['week']
        date_finish = data_json['date_finish']
        
        if not date_finish == '':
            parsed_date = datetime.datetime.strptime(date_finish, "%d.%m.%Y").date()
        else:
            parsed_date = datetime.date(1970, 1, 1)

        detail = mw_Detail.objects.get(id=int(detail_id))
        work = mw_Work.objects.get(id=int(work_id))

        prg, created = mw_Progress.objects.update_or_create(detail = detail, work = work)
        prg.progress = int(oper)
        try:
            prg.week = int(week)
        except:
            prg.week = 0
        prg.date_finish = parsed_date
        prg.save()

        detail.save()
    
    return redirect('/pressforms/production/')

class DetailApiView(APIView):
    
    def get_object(self, id):
        '''Метод возвращает задание по id'''
        try:
            return mw_Detail.objects.get(id=id)
        except mw_Detail.DoesNotExist:
            return None
        
    def get_object_by_uuid(self, uuid_1C):
        '''Метод возвращает задание по uuid'''
        try:
            return mw_Detail.objects.get(uuid_1C=uuid_1C)
        except mw_Detail.DoesNotExist:
            return None
    
    def get(self, request, *args, **kwargs):
        '''Получить детали'''
        details = mw_Detail.objects.all().order_by('-date_start')
        serializer = DetailSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Создание / обновление детали'''
        data = {
            'article': request.data.get('article'),
            'assembly': request.data.get('assembly'),
            'name': request.data.get('name'),
            'full_name': request.data.get('full_name'),
            'quantity': request.data.get('quantity'),
            'uuid_1C': request.data.get('uuid_1C'),
            'date_start': request.data.get('date_start'), 
            'partner_uuid_1C': request.data.get('partner_uuid_1C'), 
        }

        partner = Partner.objects.get(uuid_1C=data['partner_uuid_1C'])
        data['partner'] = partner.id
        
        detail_instance = self.get_object_by_uuid(data['uuid_1C'])
        if not detail_instance:
            serializer = DetailSerializer(data=data)
        else:
            serializer = DetailSerializer(instance = detail_instance, data=data, partial = True)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DetailLastModifiedApiView(APIView):
        # 1. Get events 
    def get(self, request, *args, **kwargs):
        '''Получить список событий'''
        pressforms = mw_Detail.objects.all().order_by('-date_modified')[:1]
        if (pressforms.count() >= 1):
            serializer = DetailLastModifiedSerializer(pressforms[0], many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("", status=status.HTTP_200_OK)