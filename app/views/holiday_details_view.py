# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.models import exit_details_model
from app.models.location_model import Location
from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from app.models.asset_model import Asset_Detail 
from app.models.holiday_details_model import Holiday_Detail 
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.Holiday_DetailsForm import Holiday_DetailsForm
from django.conf import settings

from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
from datetime import datetime
import datetime

from django.utils import timezone

#from app.models import QuillModel



@login_required(login_url="/login/")
def holiday_details(request):
   
    holidays = Holiday_Detail.objects.filter(is_active='1', applicable_location_id__is_active = 1 )
    locations = Location.objects.filter(is_active = 1)
    # print(holidays)
    context = {'employees':holidays, 'locations': locations}
    return render(request, "holiday_details/index.html", context)



def add_holiday_details(request):  
  
    form = Holiday_DetailsForm()
   
    if request.method == 'POST':
        form = Holiday_DetailsForm(request.POST)
        #return HttpResponse('date')   
        if  form.is_valid():
            holiday_name = request.POST.get('holiday_name')
            
            applicable_location_id = request.POST.get('applicable_location')
            
            description = request.POST.get('description')
            
            date = request.POST.get('date')
            if date != "":
                  d = datetime.datetime.strptime(date, '%d-%m-%Y')
                  date = d.strftime('%Y-%m-%d')
            else:
                  date = None 

            type = request.POST.get('type')       
            #return HttpResponse(type)
            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            obj = Holiday_Detail.objects.create( 
            
                  holiday_name=holiday_name,
                  applicable_location_id=applicable_location_id,
                  description=description,
                  date=date,type=type,

            created_at=created_at, updated_at=updated_at, is_active=is_active,

            ) 
            obj.save()
            messages.success(request, 'holiday was added ! ')
            return redirect('holiday_details')

    locations = Location.objects.filter(is_active = 1) 
        
    context = {'form':form, 'locations': locations}
    return render(request, "holiday_details/add_holiday_details.html", context )
   
def delete_holiday_details(request, pk):
   # return HttpResponse('working..')
    data = Holiday_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'holiday was deleted! ')
    return redirect('holiday_details')

def edit_holiday_details(request, pk):  
  
    form = Holiday_DetailsForm()
   
    if request.method == 'POST':
        form = Holiday_DetailsForm(request.POST)
        #return HttpResponse('date')   
        if  form.is_valid():
            holiday_name = request.POST.get('holiday_name')
            
            applicable_location_id = request.POST.get('applicable_location')
            
            description = request.POST.get('description')
            
            date = request.POST.get('date')
            if date != "":
                  d = datetime.datetime.strptime(date, '%d-%m-%Y')
                  date = d.strftime('%Y-%m-%d')
            else:
                  date = None 

            type = request.POST.get('type')       
            #return HttpResponse(type)
            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            obj = Holiday_Detail.objects.filter(id=pk).update( 
            
                  holiday_name=holiday_name,
                  applicable_location_id=applicable_location_id,
                  description=description,
                  date=date,type=type,
                  updated_at=updated_at, is_active=is_active,

            ) 
           
            messages.success(request, 'holiday was updated !')
            return redirect('holiday_details')

    locations = Location.objects.filter(is_active = 1) 
    holyy = Holiday_Detail.objects.get(id = pk)    
    context = {'form':form, 'locations': locations, 'holi': holyy }
    return render(request, "holiday_details/edit_holiday_details.html", context )
   
def delete_holiday_details(request, pk):
   # return HttpResponse('working..')
    data = Holiday_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'holiday was deleted! ')
    return redirect('holiday_details')    


def filter_holiday(request):

    # return HttpResponse(request.POST.get('location'))

    locations = Location.objects.filter(is_active = 1, )

    if request.POST.get('location') =="All":
        holidays = Holiday_Detail.objects.filter(is_active='1', applicable_location_id__is_active = 1 )
    else:
        holidays = Holiday_Detail.objects.filter(is_active='1', applicable_location_id = request.POST.get('location'), applicable_location_id__is_active = 1 )

    # print(holidays[0].applicable_location.location)
    context = {'employees':holidays, 'locations': locations}
    return render(request, "holiday_details/index.html", context)