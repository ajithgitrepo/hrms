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
from django.utils import timezone
import datetime 
from datetime import datetime
from django.db.models import Q

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
                checkout_time = datetime.now().strftime('%H:%M:%S'),
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


