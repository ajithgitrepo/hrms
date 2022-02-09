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
#from app.forms import UserGroupForm

from django.contrib.auth.models import User
# from app.models import Group

#from app.models import Group
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
from datetime import datetime, timedelta
from app.models.attendance_model import Attendance

from app.models.employee_model import Employee
from app.models.workhome_model import Workhome
from app.forms.WorkhomeForm import WorkhomeForm



from dateutil import relativedelta
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.files import File as DjangoFile
import os
from django.conf import settings

from app.views.self_service_view import attendance



def workhome_requests(request):
   # return HttpResponse("employee")
    workhome = Workhome.objects.filter(is_active='1',employee=request.user.emp_id)

    context = {'workhome_requests': workhome}
    return render(request, "workhome/index.html", context)


def add_workhome_request(request):

    form = WorkhomeForm()
    if request.method == 'POST':
        form = WorkhomeForm(request.POST)
        if form.is_valid():
            # print(request.user.emp_id)
            # employee = request.user.emp_id
            date = request.POST.get('start_date')
            start_date= datetime.strptime(date, "%d-%m-%Y").strftime('%Y-%m-%d')
            # print(start_date)
            to_date = request.POST.get('end_date')
            end_date= datetime.strptime(to_date, "%d-%m-%Y").strftime('%Y-%m-%d')
            # print(end_date)

            reason = request.POST.get('reason')
            # diff = abs((end_date-start_date).days)+1
            wfh_start=datetime.strptime(date, "%d-%m-%Y")
            wfh_end=datetime.strptime(to_date, "%d-%m-%Y")
            # print(wfh_start,wfh_end)
            
            delta = wfh_end - wfh_start       # as timedelta

            # print(delta)
           
            obj = Workhome.objects.create(    start_date=start_date,
                                              end_date=end_date,
                                              reason=reason,
                                              employee=Employee.objects.get(employee_id = request.user.emp_id) if request.user.emp_id else None, 
                                              created_by=Employee.objects.get(employee_id = request.user.emp_id) if request.user.emp_id else None,
                                         )
            for i in range(delta.days + 1):
                day = wfh_start + timedelta(days=i)  

                attendance=Attendance.objects.create(date=datetime.strftime(day, "%Y-%m-%d"),
                                         employee_id=request.user.emp_id,
                                         is_present=0,
                                         is_active=1,  
                                         is_wfh_approved=0, 
                                         created_at=timezone.now()
                                         )                             
            messages.success(request,' Work From Home was requested! ')
            return redirect('workhome_requests')  
    

                                                         
    context = {'form': form}
    return render(request, "workhome/add_workhome_request.html", context)


def delete_workhome(request, pk):
    # return HttpResponse('working..')
    data = Workhome.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, 'Work From Home was deleted! ')
    return redirect('workhome_requests')