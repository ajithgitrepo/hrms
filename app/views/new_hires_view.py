# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.views.employee_view import employees
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.EmployeeForm import EmployeeForm 
from app.forms.LeaveTypeForm import LeaveTypeForm

#from app.forms import UserGroupForm  

from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
from app.models.leave_type_model import * 
from app.models.leave_balance_model import *
from app.models.department_model import *
from app.models.role_model import *
# from app.models.leave_balance_model import *
# from app.models import Group 

#from app.models import Group 
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q, query
from datetime import datetime
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
import MySQLdb
from itertools import chain
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.db import connection,transaction
from django.db.models import F
from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
import datetime
from app.models.attendance_model import Attendance
from django.http import JsonResponse
import json

#from app.models import QuillModel


@login_required(login_url="/login/")
def index(request):
    # query = Employee.objects.filter(role__is_active ='1', department__is_active ='1', birth_date= datetime.date.today() )

    # last 15 days records
    new_hires = Employee.objects.filter(is_active = 1, role__is_active ='1', department__is_active ='1', created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=15))
    # print(new_hires)
    
    # last 3 records
    # new_hires = Employee.objects.filter(is_active = 1).order_by('-created_at')[:3]
    # print(new_hires)
    
   
    context = {
        # 'birthdays': query,
        'new_hires':new_hires
    }

    return render(request, "new_hires/index.html", context)


@login_required(login_url="/login/")
def birthdays(request):

    current_month = datetime.datetime.now().month
    day = datetime.datetime.now().day
 
    query = Employee.objects.filter(role__is_active ='1', department__is_active ='1', birth_date__month=current_month, birth_date__day=day).values('employee_id', 'first_name', 'last_name', 'email_id', 'birth_date', 'department__name', 'role__name')
    # print(query)
    context = {
        'birthdays': query,
    }

    return render(request, "new_hires/birthdays.html", context)


@login_required(login_url="/login/")
def get_birthday(request):

    date_request = datetime.datetime.strptime(request.POST.get('date_get'), "%d-%m-%Y")
    month = date_request.strftime('%m')
    date = date_request.strftime('%d')

    query = list(Employee.objects.filter(role__is_active ='1', department__is_active ='1', birth_date__month=month, birth_date__day=date).values('employee_id', 'first_name', 'last_name', 'email_id', 'department__name', 'role__name'))
    # print(query)

    # queryJson = serializers.serialize("json",query)
    # Obj = json.loads(queryJson)
    # # print(Obj)

    context = {
        'birthdays': query,
        'date': request.POST.get('date_get'),
    }

    # return JsonResponse(context)

    return HttpResponse( json.dumps(context) )

    
