
from django import http
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.EmployeeForm import EmployeeForm
from app.models.department_model import Department
from app.models.timelogs import TimeLogs
from app.views.project_view import projects
from app.views.restriction_view import admin_only,role_name

from app.models.employee_model import Employee, Work_Experience, Education, Dependent
from app.models.reporting_to_model import Reporting
from django.contrib.auth.models import User

from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q, manager

from django.utils import timezone
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
import MySQLdb
from itertools import chain

from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.hashers import make_password, check_password

from app.models.employee_model import Employee
from app.models.client_model import Client
from app.models.project_model import Project
from app.forms.ProjectForm import ProjectForm

from dateutil import relativedelta
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.files import File as DjangoFile
import os
import datetime 
from datetime import date, time, datetime, timedelta
from django.conf import settings
import calendar


def timelogs(request):

    now = datetime.now()
    first_day = now.replace(day = 1)
    last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])
    role = role_name(request)
    # print(role)
    timelogs = TimeLogs.objects.filter(is_active='1', employee_id = request.user.emp_id, project__is_active = 1, date__range=[first_day, last_day])
    # print(timelogs)


    projects = Project.objects.filter(is_active = 1, project_users__contains=request.user.emp_id)
    
    context = {
        'timelogs': timelogs,
        'projects': projects,
        'month_no': now.strftime("%m"),
        'year': now.strftime("%Y"),
    }

    return render(request, "timelogs/index.html", context)


def timelog_checkin(request):
    if request.method == 'POST':
        print(request.POST.get('project_id'))
        myDate = datetime.now()
        if not TimeLogs.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, project_id = request.POST.get('project_id'),  is_active = 1)).exists():
            insert = TimeLogs.objects.create(
                date=myDate, 
                working_on = request.POST.get('working_on'),
                start_time= datetime.now().strftime('%H:%M:%S'), 
                project_id = request.POST.get('project_id'),
                is_active = 1,
                decription = request.POST.get('decription'),
                employee_id= request.user.emp_id,
            )
            request.session['timelogin_session'] = datetime.now().strftime('%H:%M:%S')
            request.session['time_project_session'] = request.POST.get('project_id')
            messages.success(request,' Timelog updated successfully ')
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            update = TimeLogs.objects.filter(date=myDate, employee_id= request.user.emp_id, project_id = request.POST.get('project_id'), is_active = 1 ).update(
                is_active = 1,
            )
            messages.success(request,' Timelog updated successfully ')
            request.session['timelogin_session'] = datetime.now().strftime('%H:%M:%S')
            request.session['time_project_session'] = request.POST.get('project_id')

    return redirect(request.META.get('HTTP_REFERER'))


def timelog_checkout(request):
    if request.method == 'POST':
        myDate = datetime.now()
        
        if TimeLogs.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, project_id = request.session.get('time_project_session'), is_active = 1)).exists():
            update = TimeLogs.objects.filter(date=myDate, employee_id= request.user.emp_id ).update(
                end_time = datetime.now().strftime('%H:%M:%S'),
                updated_at = datetime.now(),
                
            )
            del request.session['timelogin_session']
            messages.success(request,' Timelog updated successfully ')
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            del request.session['timelogin_session']
            messages.success(request,' Timelog updated successfully ')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

def filter_timelog(request, month):
    
    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")

    date = datetime.strptime(month, "%m-%Y")
    first_day = date.replace(day=1)
    last_day = date.replace(day=calendar.monthrange(date.year, date.month)[1])

    myDate = datetime.today()

    timelogs = TimeLogs.objects.filter(is_active='1', employee_id = request.user.emp_id, project__is_active = 1, date__range=[first_day, last_day])
    # print(timelogs)

    projects = Project.objects.filter(is_active = 1, project_users__contains=request.user.emp_id)
    # print(projects)

    context = {
        'timelogs': timelogs,
        'projects': projects,
        'month_no': date.strftime("%m"),
        'year': date.strftime("%Y"),
    }

    return render(request, "timelogs/index.html", context)


def click_timelog_dahsboard(request):
    timelogs = TimeLogs.objects.filter(is_active = 1, date = request.POST.get('date'), employee_id = request.user.emp_id, project__is_active = 1)
    # project_name = timelogs[0].project.project_name

    obj = []

    obj.append({'project': timelogs[0].project.project_name, 'start_time': timelogs[0].start_time,'end_time': timelogs[0].end_time,'created_at': timelogs[0].created_at,'updated_at': timelogs[0].updated_at, })
     
    # final_list_arr = list(chain(timelogs))
    
    # jsondata = serializers.serialize('json', obj)
    # print(obj)

    return HttpResponse(obj)

def time_logs(request):
    now = datetime.now()
    first_day = now.replace(day = 1)
    last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])
    role = role_name(request)
    # print(role)

    if role=="Admin":
        timelogs = TimeLogs.objects.filter(is_active='1', employee_id = request.user.emp_id, project__is_active = 1, date__range=[first_day, last_day])
        # print(timelogs)
        projects = Project.objects.filter(is_active = 1)
        # print(projects)
        reporting = Employee.objects.filter(is_active = 1)
        # print(projects)

    if role=="Manager":
        timelogs = TimeLogs.objects.filter(is_active='1', employee_id = request.user.emp_id, project__is_active = 1, date__range=[first_day, last_day])
        # print(timelogs)
        projects = Project.objects.filter(is_active = 1, project_manager_id = request.user.emp_id)
        # print(projects)
        reporting = Reporting.objects.select_related().filter(Q(is_active=1) & Q(reporting_id=request.user.emp_id) )
        # print(reporting)


    context = {
        'timelogs': timelogs,
        'projects': projects,
        'month_no': now.strftime("%m"),
        'year': now.strftime("%Y"),
        'employees':reporting,
    }

    return render(request, "timelogs/admin/index.html", context)


def search_timelog(request,pk,month):

    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    date = datetime.strptime(month, "%m-%Y")
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    role = role_name(request)
    # print(role)
    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append( (first_day + timedelta(days=i)) )
        date_no.append( (first_day + timedelta(days=i)).strftime("%d") )

    if role=="Admin":
        timelogs = TimeLogs.objects.filter(is_active='1', employee_id = pk, project__is_active = 1, date__range=[first_day, last_day])
        # print(timelogs)
        projects = Project.objects.filter(is_active = 1)
        # print(projects)
        reporting = Employee.objects.filter(is_active = 1)
        # print(projects)

    if role=="Manager":
        timelogs = TimeLogs.objects.filter(is_active='1', employee_id = pk, project__is_active = 1, date__range=[first_day, last_day])
        # print(timelogs)
        projects = Project.objects.filter(is_active = 1, project_manager_id = request.user.emp_id)
        # print(projects)
        reporting = Reporting.objects.select_related().filter(Q(is_active=1) & Q(reporting_id=request.user.emp_id) )
        # print(reporting)

    context = {
        'timelogs': timelogs,
        'projects': projects,
        'month_no': date.strftime("%m"),
        'year': date.strftime("%Y"),
        'employees':reporting,
        'emp_id':pk,
    }

    return render(request, "timelogs/admin/index.html", context)
