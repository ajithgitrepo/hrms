# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.models import exit_details_model
from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from app.models.asset_model import Asset_Detail
from app.models.employee_model import Employee
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.Asset_DetailsForm import Asset_DetailForm
from django.conf import settings

#from app.forms import UserGroupForm  

# from app.models.employee_model import Onboard_Employee , 
# from app.models import Group 

#from app.models import Group 
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

def asset_details(request):
   # return HttpResponse("employee")
    employee = Asset_Detail.objects.filter(is_active='1')
#     Asset_Detail.objects.select_related('employee').get(is_active='1')
   # return HttpResponse(employee)
    print(employee)
    context = {'employees':employee}
    return render(request, "asset_details/index.html", context)


def snippets_asset_all_info(request):
    
    emp_id =    request.POST.get('emp_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
   
    final_list = Asset_Detail.objects.filter(employee_id = emp_id)
   
    jsondata = serializers.serialize('json', final_list)
 
    return HttpResponse(jsondata, content_type='application/json')
  


def add_asset_details(request):  
   # return HttpResponse('working..') 
   # return render(request, "exit_details/add_exit_details.html")
    form = Asset_DetailForm()
    #return HttpResponse(request.method)
   # """
    if request.method == 'POST':
        form = Asset_DetailForm(request.POST)
        if  form.is_valid():
           
            employee = request.POST.get('employee')
           
           
           
            type_of_asset = request.POST.get('type_of_asset')
          #  return HttpResponse(employee)
            asset_details = request.POST.get('asset_details')
            
            given_date = request.POST.get('given_date')
            if given_date != "":
               #return HttpResponse(date)   
               d = datetime.datetime.strptime(given_date, '%d-%m-%Y')
               given_date = d.strftime('%Y-%m-%d')
            else:
               given_date = None  

            return_date = request.POST.get('return_date')
            if return_date != "":
               #return HttpResponse(date)   
               d = datetime.datetime.strptime(return_date, '%d-%m-%Y')
               return_date = d.strftime('%Y-%m-%d')
            else:
               return_date = None    
            
            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            # if not Asset_Detail.objects.filter( Q(employee=employee)).exists():
            obj = Asset_Detail.objects.create( 
            employee_id=employee, 
            
            type_of_asset=type_of_asset,

            given_date=given_date,
            return_date=return_date,
            asset_details=asset_details,

            created_at=created_at, updated_at=updated_at, is_active=is_active,

            ) 
               # return HttpResponse(employee)   
            obj.save()
            messages.success(request, 'asset details was added ! ')
            return redirect('asset_details') 
            # else: 
            #     employee = Employee.objects.all()
            #     context_role = {
            #             'employees': employee,
                     
            #             }
          
            #     context_role.update({"form":form})  
            #     messages.error(request, ' Asset Details Already Exists! ', context_role)
            #     context = {'form':form}
            #     return render(request, "asset_details/add_asset_details.html", context)
                
           
    employee = Employee.objects.all()
    context_role = {
          'employees': employee,
         #  'country': 'in'
       }
   
    #
   # tes = Group.objects.all()
    context_role.update({"form":form})
    print(context_role)
    return render(request, "asset_details/add_asset_details.html",  context_role )
   
def delete_asset_details(request, pk):
   # return HttpResponse('working..')
    data = Asset_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'asset was deleted! ')
    return redirect('asset_details')