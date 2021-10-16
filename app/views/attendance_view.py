# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import http
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.utils import timezone
from app.models.employee_model import Employee
import datetime 
from datetime import datetime, timedelta
from django.db.models import Q
import calendar
from app.models.attendance_model import Attendance 
from django.contrib.auth.models import Group

#from app.models import QuillModel


@login_required(login_url="/login/")
def index(request):
   
    context = {}
    context['segment'] = 'index' 

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

def check_in_attn(request):
    if request.method == 'POST':
        myDate = datetime.now()
        if not Attendance.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, checkin_time__isnull=False)).exists():
            insert = Attendance.objects.create(date=myDate, checkin_time=datetime.now().strftime('%H:%M:%S'), employee_id= request.user.emp_id)
            request.session['checkin_session'] = datetime.now().strftime('%H:%M:%S')
            messages.success(request,' Checked in successfully ')
            return redirect('home')
        else:
            update = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id ).update(
                updated_at = datetime.now(),
            )
            request.session['checkin_session'] = datetime.now().strftime('%H:%M:%S')
            # print(request.session['checkin_session'])

    return redirect('home')

def check_out_attn(request):
    if request.method == 'POST':
        myDate = datetime.now()
        if Attendance.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, checkin_time__isnull=False)).exists():
            update = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id ).update(
                checkout_time = datetime.now().strftime('%H:%M:%S'),
                updated_at = datetime.now(),
            )
            del request.session['checkin_session']
            messages.success(request,' Checked out successfully ')
            return redirect('home')

        else:
            del request.session['checkin_session']
            messages.success(request,' Checked out successfully ')
            return redirect('home')

    return redirect('home')


def attn_listview(request):

    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    first_day = now.replace(day = 1)
    last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])
    # no_of_days = calendar.monthrange(current_year, current_month )
    
    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append( (first_day + timedelta(days=i)) )
        date_no.append( (first_day + timedelta(days=i)).strftime("%d") )

    month_atten = Attendance.objects.filter(is_active = 1,  employee_id = request.user.emp_id, date__range=[first_day, last_day])
    # print(month_atten)

    present_days = Attendance.objects.filter(is_active = 1, is_present = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(present_days)

    absent_days = Attendance.objects.filter(is_active = 1, is_leave = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(absent_days)

    zipped_data = zip(dates, date_no)
#    print(zipped_data)
    employees = Employee.objects.filter(is_active = 1)
 
    context = {
        'month_atten':month_atten,
        'zipped_data':zipped_data,
        'employees':employees,
        'present_days':present_days,
        'absent_days':absent_days,

    }

    return render(request, "attendance/attn_list.html",context)

def search_listview(request,pk):
    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    first_day = now.replace(day = 1)
    last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])
    # no_of_days = calendar.monthrange(current_year, current_month )
    
    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append( (first_day + timedelta(days=i)) )
        date_no.append( (first_day + timedelta(days=i)).strftime("%d") )

    month_atten = Attendance.objects.filter(is_active = 1,  employee_id = pk, date__range=[first_day, last_day])
    # print(month_atten)

    zipped_data = zip(dates, date_no)
#    print(zipped_data)
    employees = Employee.objects.filter(is_active = 1)
 
    context = {
        'month_atten':month_atten,
        'zipped_data':zipped_data,
        'employees':employees,
        'search_id':pk,

    }

    return render(request, "attendance/attn_list.html",context)