# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from app.forms.TaskForm import TaskForm
from django.utils import timezone
import datetime
import calendar
from datetime import datetime
from django.core import serializers
from django.http import JsonResponse


#from app.forms import UserGroupForm  

from app.models.task_model import Task
from app.models.employee_model import Employee 
# from app.models import Group 
from django.conf import settings

from django.contrib.auth.models import Group
from django.db.models import Max, Subquery, OuterRef

from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q
# from datetime import datetime
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
from django.core.paginator import Paginator,InvalidPage, EmptyPage
from itertools import chain

# from django.utils import timezone



# @login_required(login_url="/login/")
# def index(request):
    
#     context = {}
#     context['segment'] = 'index' 

#     html_template = loader.get_template( 'index.html' )
#     return HttpResponse(html_template.render(context, request))


# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:
        
#         load_template      = request.path.split('/')[-1]
#         context['segment'] = load_template
        
#         html_template = loader.get_template( load_template )
#         return HttpResponse(html_template.render(context, request))
        
#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template( 'page-404.html' )
#         return HttpResponse(html_template.render(context, request))

#     except:
    
#         html_template = loader.get_template( 'page-500.html' )
#         return HttpResponse(html_template.render(context, request))

def tasks(request):
#     print('it works')
    date1=datetime.today().replace(day=1)
    date2=datetime.today().replace(day = calendar.monthrange(datetime.today().year, datetime.today().month)[1])
    #print(date2)
#     this_month=[date1,date2]
#     print(this_month)
    tasks = Task.objects.filter( Q(is_active=1,start_date__range=(date1,date2),end_date__range=(date1,date2) ))
#     paginator = Paginator(tasks, 5)
#     print(paginator)# Show 25 contacts per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    page = request.GET.get('page', 1)

    paginator = Paginator(tasks, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    context = {'tasks':tasks ,'users':users}
#     print(context)


    return render(request, "task/index_task.html", context)



def add_task(request):
    #return HttpResponse('it works')
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
#         print('34567')
        if form.is_valid():
            print('34567')
            employee  = request.POST.get('employee')
            #return HttpResponse(employee_id)
            task_name = request.POST.get('task_name')
            description = request.POST.get('description')
            date = request.POST.get('start_date')
            start_date= datetime.strptime(date, "%d-%m-%Y").strftime('%Y-%m-%d')

#             print(start_date)

            to_date = request.POST.get('end_date')
            end_date= datetime.strptime(to_date, "%d-%m-%Y").strftime('%Y-%m-%d')
            notify_date = request.POST.get('reminder')
            reminder= datetime.strptime(notify_date, "%d-%m-%Y").strftime('%Y-%m-%d')
            priority = request.POST.get('priority')
            status = request.POST.get('status')
            is_active = '1'
            device = 'web'
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # print(form.errors)
            # print(role_name)
            g1 = Task.objects.create(employee_id=employee, task_name=task_name, description=description,
                start_date=start_date, end_date=end_date, reminder=reminder, priority=priority,
                status=status,is_active=is_active, device=device, created_at=created_at)
            g1.save()
            messages.success(request,'Task added successfully ! ')
            return redirect('tasks')
    # print(form.errors)
#     context = {'form':form}

    employee = Employee.objects.filter(is_active='1')
    context_role = {
            'employees': employee,
           }
    #print(context_role)
    context_role.update({"form":form, 'employee':employee})
    #return HttpResponse(employee)
    return render(request, "task/add_task.html", context_role)

def update_task(request, pk):
    tasks = Task.objects.get(id=pk)
    form = TaskForm(instance=tasks)
    # print(role)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=tasks)
        if form.is_valid():

            employee_id  = request.POST.get('employee_id')
            task_name = request.POST.get('task_name')
            description = request.POST.get('description')
            date = request.POST.get('start_date')
            start_date= datetime.strptime(date, "%d-%m-%Y").strftime('%Y-%m-%d')

#             print(start_date)

            to_date = request.POST.get('end_date')
            end_date= datetime.strptime(to_date, "%d-%m-%Y").strftime('%Y-%m-%d')
            notify_date = request.POST.get('reminder')
            reminder= datetime.strptime(notify_date, "%d-%m-%Y").strftime('%Y-%m-%d')
            priority = request.POST.get('priority')
            status = request.POST.get('status')

            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # print(form.errors)
            # print(role_name)
            g1 = Task.objects.filter(id=pk).update(employee_id=employee_id, task_name=task_name, description=description,
                     start_date=start_date, end_date=end_date, reminder=reminder, priority=priority,status=status,updated_at=updated_at)
#             task.updated_at = timezone.now()
#             tasks.save()

            messages.success(request, ' Task was updated! ')
            return redirect('tasks')
    context = {'task':tasks}

    employee = Employee.objects.filter(is_active='1')
    context_role = {
            'employees': employee,
           }
    context_role.update({'task':tasks, 'employee':employee})

    return render(request, "task/update_task.html", context_role)



def delete_task(request, pk):
    # return HttpResponse('working..')
    data = Task.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.error(request, ' Task was deleted! ')
    return redirect('tasks')

# def search(request):
#     if request.method == 'GET': # this will be GET now
#         filter_value =  request.GET.get('search') # do some research what it does
#         book_name=Task.objects.get(filter_value)
#         try:
#             status = Task.objects.filter(task_name=book_name)
#         #Add_prod class contains a column called 'bookname'
#         except Task.DoesNotExist:
#             status = None
#         return render(request,"task/index_task.html",{"books":status})
#     else:
#         return render(request,"task/index_task.html",{})
def search(request):

        query = request.GET.get("search")
#         print(query)

        if query =="":
#             print('fdf')
            date1=datetime.today().replace(day=1)
            date2=datetime.today().replace(day = calendar.monthrange(datetime.today().year, datetime.today().month)[1])

            tasks = Task.objects.filter( Q(is_active=1,start_date__range=(date1,date2),end_date__range=(date1,date2) ))
            page = request.GET.get('page', 1)

            paginator = Paginator(tasks, 5)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            users=users

        else:
            users = Task.objects.filter(Q(task_name=query) | Q(employee=query))


        context = {
        'users':users
        }
        template = 'task/index_task.html'
        return render(request, template, context)


