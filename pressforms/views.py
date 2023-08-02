from django.http import Http404
from django.shortcuts import render, redirect
from .models import Pressform, TypeWork, Work, Progress
from .forms import PressformForm
from django.db.models import Count

def history(request):
    """ Формирование произведенных прессформ """
    pressform_list = Pressform.objects.order_by('date_finish')
    years = Pressform.objects.filter(year__gt=0).values('year').annotate(dcount=Count('year')).order_by('-year')

    max_item = 0
    for year in years:
        max_item = max(max_item, year['dcount'])

    context = {
        'pressform_list': pressform_list,
        'years': years,
        'max_item': max_item,
    }

    return render(request, 'pressforms/history.html', context)

def pressforms(request):
    """ Формирует список всех прессформ """
    pressforms_list = Pressform.objects.order_by('-id')
    context = {'pressforms': pressforms_list}
    return render(request, 'pressforms/pressforms.html', context)

def production(request):
    """ Формирует план производства прессформ """
    pressforms = Pressform.objects.filter(year=0).order_by('date_finish')
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
                
                for prg in progress:
                    if prg.pressform == pf and prg.work == work:
                        data_work['progress'] = prg.progress
                        data_work['week'] = prg.week
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

def operation(request):
    """ Сохраняет введенные данные """
    if request.method == 'POST':
        #print(request.POST)
        pressform_id = request.POST['pressform_id']
        work_id = request.POST['work_id']
        oper = request.POST['oper']
        week = request.POST['week']

        pressform = Pressform.objects.get(id=int(pressform_id))
        work = Work.objects.get(id=int(work_id))

        prg, created = Progress.objects.update_or_create(pressform = pressform, work = work)
        prg.progress = int(oper)
        prg.week = int(week)
        prg.save()
 
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