# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.models import exit_details_model
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
def index(request):
    
    context = {}
    context['segment'] = 'index' 

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

def holiday_details(request):
   
    employee = Holiday_Detail.objects.filter(is_active='1')
#     Asset_Detail.objects.select_related('employee').get(is_active='1')
    print(employee)
    context = {'employees':employee}
    return render(request, "holiday_details/index.html", context)



def add_holiday_details(request):  
  
    form = Holiday_DetailsForm()
   
    if request.method == 'POST':
        form = Holiday_DetailsForm(request.POST)
        #return HttpResponse('date')   
        if  form.is_valid():
            #return HttpResponse('date')   
            holiday_name = request.POST.get('holiday_name')
            
            applicable_location = request.POST.get('applicable_location')
            
            description = request.POST.get('description')
            
            date = request.POST.get('date')
            if date != "":
                  #return HttpResponse(date)   
                  d = datetime.datetime.strptime(date, '%d-%m-%Y')
                  date = d.strftime('%Y-%m-%d')
            else:
                  date = None  

            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            # if not Asset_Detail.objects.filter( Q(employee=employee)).exists():
            obj = Holiday_Detail.objects.create( 
            
                  holiday_name=holiday_name,
                  applicable_location=applicable_location,
                  description=description,
                  date=date,

            created_at=created_at, updated_at=updated_at, is_active=is_active,

            ) 
            # return HttpResponse(employee)   
            obj.save()
            messages.success(request, 'holiday was added ! ')
            return redirect('holiday_details') 
            # else: 
            #     employee = Employee.objects.all()
            #     context_role = {
            #             'employees': employee,
                     
            #             }
          
            #     context_role.update({"form":form})  
            #     messages.error(request, ' Asset Details Already Exists! ', context_role)
            #     context = {'form':form}
            #     return render(request, "asset_details/add_asset_details.html", context)
                
#     employee = Employee.objects.all()
      #   context_role = {
      #         "form":form,
      #       }
      
#     #
#    # tes = Group.objects.all()
   #  context_role.update({"form":form})
#     print(context_role)
    context = {'form':form}
    return render(request, "holiday_details/add_holiday_details.html", context )
   
def delete_holiday_details(request, pk):
   # return HttpResponse('working..')
    data = Holiday_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'holiday was deleted! ')
    return redirect('holiday_details')