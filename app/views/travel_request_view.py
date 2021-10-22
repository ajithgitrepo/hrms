# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.models import exit_details_model
from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from app.models.travel_request_model import Travel_Request_Detail
from app.models.employee_model import Employee
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.TarvelRequest_DetailsForm import TarvelRequest_DetailForm
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

def travel_request_details(request):
   # return HttpResponse("employee")
    employee = Travel_Request_Detail.objects.filter(is_active='1').order_by('-created_at')
#     Asset_Detail.objects.select_related('employee').get(is_active='1')
   # return HttpResponse(employee)
    print(employee)
    context = {'employees':employee}
    return render(request, "travel_request_details/index.html", context)


def snippets_travel_details_employee_all_info(request):
    
    id =    request.POST.get('emp_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
   
    final_list = Travel_Request_Detail.objects.filter(id = id)
   
    jsondata = serializers.serialize('json', final_list)
 
    return HttpResponse(jsondata, content_type='application/json')
  


def add_travel_request_details(request):  
    #return HttpResponse('working..') 
   # return render(request, "exit_details/add_exit_details.html")
    form = TarvelRequest_DetailForm()
   # return HttpResponse(form)
   # """
    if request.method == 'POST':
        form = TarvelRequest_DetailForm(request.POST)
        if  form.is_valid(): 
           # return HttpResponse('working..') 
            employee = request.POST.get('employee')
           
            place_of_visit = request.POST.get('place_of_visit')
           # return HttpResponse(place_of_visit)
            employee_department = request.POST.get('employee_department')
            
            expected_date_of_arrival = request.POST.get('expected_date_of_arrival')
            if expected_date_of_arrival != "":
               #return HttpResponse(date)   
               d = datetime.datetime.strptime(expected_date_of_arrival, '%d-%m-%Y')
               expected_date_of_arrival = d.strftime('%Y-%m-%d')
            else:
               expected_date_of_arrival = None  

            expected_date_of_depature = request.POST.get('expected_date_of_depature')
            if expected_date_of_depature != "":
               #return HttpResponse(date)   
               d = datetime.datetime.strptime(expected_date_of_depature, '%d-%m-%Y')
               expected_date_of_depature = d.strftime('%Y-%m-%d')
            else:
               expected_date_of_depature = None   

            expected_duration_days = request.POST.get('expected_duration_days')

            purpose_of_visit = request.POST.get('purpose_of_visit')

            billable_to_customer = request.POST.get('billable_to_customer')


            customer_name = request.POST.get('customer_name')    
            
            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            # if not Asset_Detail.objects.filter( Q(employee=employee)).exists():
            obj = Travel_Request_Detail.objects.create( 

            employee_id=employee, 
            place_of_visit=place_of_visit,
            expected_date_of_arrival=expected_date_of_arrival,
            expected_date_of_depature=expected_date_of_depature,
            expected_duration_days=expected_duration_days,
            purpose_of_visit=purpose_of_visit,
            customer_name=customer_name,
            employee_department=employee_department,
            billable_to_customer=billable_to_customer,
            created_at=created_at, updated_at=updated_at, is_active=is_active,

            ) 
               # return HttpResponse(employee)   
            obj.save()
            messages.success(request, 'travel request details was added ! ')
            return redirect('travel_request_details') 
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
    return render(request, "travel_request_details/add_travel_request_details.html",  context_role )
   
def delete_asset_details(request, pk):
   # return HttpResponse('working..')
    data = Travel_Request_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'travel request was deleted! ')
    return redirect('travel_request_details')