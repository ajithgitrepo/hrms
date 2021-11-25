# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#from app.models import compensatory_request_model
#from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from app.models.compensatory_request_model import Compoensatory_Request_Detail
from app.models.employee_model import Employee
from django.contrib.auth.decorators import login_required
#from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
#from django.http import HttpResponseRedirect
from app.forms.CompensatoryRequest_DetailsForm import CompensatoryRequest_DetailForm
from django.conf import settings
from app.views.restriction_view import admin_only,role_name
from app.models.attendance_model import Attendance 

#from app.models import Group 
from django.conf.urls import url
#from pprint import pprint
from django.shortcuts import render
# from django.template import RequestContext
from django.db.models import Q
from datetime import datetime
# from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection

import datetime

from django.utils import timezone



@login_required(login_url="/login/")
def compensatory_request_details(request):
    employee = Compoensatory_Request_Detail.objects.filter(is_active='1').order_by('-created_at')
    # print(employee)
    context = {'employees':employee}
    return render(request, "compensatory_request_details/index.html", context)


def snippets_compensatory_details_employee_all_info(request):
    
    id =    request.POST.get('emp_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
   
    final_list = Compoensatory_Request_Detail.objects.filter(id = id)
    # print(final_list)
    jsondata = serializers.serialize('json', final_list)
 
    return HttpResponse(jsondata, content_type='application/json')
  


def add_compensatory_request_details(request):  
    #return HttpResponse('working..') 
   # return render(request, "exit_details/add_exit_details.html")
    form = CompensatoryRequest_DetailForm()
    
   # """
    if request.method == 'POST':
        form = CompensatoryRequest_DetailForm(request.POST)
        if  form.is_valid(): 
            employee = request.POST.get('employee')
            unit = request.POST.get('unit')
            duration = request.POST.get('duration')
            
            worked_date = request.POST.get('worked_date')
            if worked_date != "":
               d = datetime.datetime.strptime(worked_date, '%d-%m-%Y')
               worked_date = d.strftime('%Y-%m-%d')
            else:
               worked_date = None  

            compoensatory_date = request.POST.get('compoensatory_date')
            if compoensatory_date != "":
               d = datetime.datetime.strptime(compoensatory_date, '%d-%m-%Y')
               compoensatory_date = d.strftime('%Y-%m-%d')
            else:
               compoensatory_date = None  

            expiry_date = request.POST.get('expiry_date')
            if expiry_date != "": 
               d = datetime.datetime.strptime(expiry_date, '%d-%m-%Y')
               expiry_date = d.strftime('%Y-%m-%d')
            else:
               expiry_date = None   

            ftime = request.POST.get('clockpicker_one')
            
            from_time = datetime.datetime.strptime(ftime, '%H:%M:%S')
            ttime = request.POST.get('clockpicker_two')
 

            to_time = datetime.datetime.strptime(ttime, '%H:%M:%S')

            reason = request.POST.get('reason')


           # customer_name = request.POST.get('customer_name')    
            
            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'

            # if not Asset_Detail.objects.filter( Q(employee=employee)).exists():
            obj = Compoensatory_Request_Detail.objects.create( 

            employee_id=employee, 
            worked_date=worked_date,
            compoensatory_date=compoensatory_date,
            unit=unit,
            duration=duration,
            from_time=from_time,
            to_time=to_time,
            expiry_date=expiry_date,
            reason=reason,
            created_at=created_at, updated_at=updated_at, is_active=is_active,

            ) 
            obj.save()
            messages.success(request, 'Compensatory request details was added ! ')
            return redirect('compensatory_request_details') 
           
    employee = Employee.objects.all()
    context_role = {
          'employees': employee,
       }
   
    #
   # tes = Group.objects.all()
    context_role.update({"form":form})
    # print(context_role)
    return render(request, "compensatory_request_details/add_compensatory_request_details.html",  context_role )
   
def delete_compensatory_details(request, pk):
   # return HttpResponse('working..')
    role = role_name(request)
    # print(role)
    data = Compoensatory_Request_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'compensatory request was deleted! ')
    if role == "Admin":
        return redirect('compensatory_request_details')
    else:
        return redirect('compensatory_request')

def compensatory_request_status(request):
    id = request.POST.get('id')
    value = request.POST.get('value')

    data = Compoensatory_Request_Detail.objects.get(id = id)
    # print(data)

    attn_data = Attendance.objects.filter(date = data.worked_date, employee_id = data.employee_id)
    # print(attn_data)

    attn = Attendance.objects.filter(date = data.compoensatory_date, employee_id = data.employee_id)

    created_at = datetime.datetime.combine(data.compoensatory_date, data.from_time)
    updated_at = datetime.datetime.combine(data.compoensatory_date, data.to_time)
    
    if attn:
        update = Attendance.objects.filter(date = data.compoensatory_date, employee_id = data.employee_id ).update(
            is_present = 2,
            is_leave=0,
            checkin_time=data.from_time.strftime('%H:%M:%S'), 
            checkout_time=data.to_time.strftime('%H:%M:%S'), 
            created_at = created_at,
            updated_at= updated_at
        )
        if update:
            data.status = value
            data.save()

            if attn_data:
                update = Attendance.objects.filter(date = data.worked_date, employee_id = data.employee_id ).update(
                    is_active=0,
                    checkin_time=data.from_time.strftime('%H:%M:%S'), 
                    checkout_time=data.to_time.strftime('%H:%M:%S'), 
                    updated_at=timezone.now()
                )


    else:
        insert = Attendance.objects.create(
            date = data.compoensatory_date,
            is_present = 2,
            is_leave=0,
            employee_id = data.employee_id,
            checkin_time=data.from_time.strftime('%H:%M:%S'), 
            checkout_time=data.to_time.strftime('%H:%M:%S'), 
            created_at = created_at,
            updated_at= updated_at
        )
        if insert:
            data.status = value
            data.save()

            if attn_data:
                update = Attendance.objects.filter(date = data.worked_date, employee_id = data.employee_id ).update(
                    is_active=0,
                    checkin_time=data.from_time.strftime('%H:%M:%S'), 
                    checkout_time=data.to_time.strftime('%H:%M:%S'), 
                    updated_at=timezone.now()
                )


    return HttpResponse(1)