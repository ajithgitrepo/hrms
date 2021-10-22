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

#from app.forms import UserGroupForm  

# from app.models.employee_model import Onboard_Employee , 
# from app.models import Group 

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

def compensatory_request_details(request):
   # return HttpResponse("employee")
    employee = Compoensatory_Request_Detail.objects.filter(is_active='1').order_by('-created_at')
    print(employee)
    context = {'employees':employee}
    return render(request, "compensatory_request_details/index.html", context)


def snippets_compensatory_details_employee_all_info(request):
    
    id =    request.POST.get('emp_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
   
    final_list = Compoensatory_Request_Detail.objects.filter(id = id)
   
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
          #  return HttpResponse('working.f.') 
            employee = request.POST.get('employee')
           #return HttpResponse(date)  
            unit = request.POST.get('unit')
           # return HttpResponse(place_of_visit)
            duration = request.POST.get('duration')
            
            worked_date = request.POST.get('worked_date')
            if worked_date != "":
               #return HttpResponse(date)   
               d = datetime.datetime.strptime(worked_date, '%d-%m-%Y')
               worked_date = d.strftime('%Y-%m-%d')
            else:
               worked_date = None  

            expiry_date = request.POST.get('expiry_date')
            if expiry_date != "":
               #return HttpResponse(date)   
               d = datetime.datetime.strptime(expiry_date, '%d-%m-%Y')
               expiry_date = d.strftime('%Y-%m-%d')
            else:
               expiry_date = None   

            ftime = request.POST.get('clockpicker_one')
           # return HttpResponse(ftime)
            
            from_time = datetime.datetime.strptime(ftime, '%H:%M:%S')
           # return HttpResponse(from_time) 
            ttime = request.POST.get('clockpicker_two')
           # return HttpResponse(from_time) 
 

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
            unit=unit,
            duration=duration,
            from_time=from_time,
            to_time=to_time,
            expiry_date=expiry_date,
            reason=reason,
            created_at=created_at, updated_at=updated_at, is_active=is_active,

            ) 
               # return HttpResponse(employee)   
            obj.save()
            messages.success(request, 'Compensatory request details was added ! ')
            return redirect('compensatory_request_details') 
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
    return render(request, "compensatory_request_details/add_compensatory_request_details.html",  context_role )
   
def delete_compensatory_details(request, pk):
   # return HttpResponse('working..')
    data = Compoensatory_Request_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'compensatory request was deleted! ')
    return redirect('compensatory_request_details')