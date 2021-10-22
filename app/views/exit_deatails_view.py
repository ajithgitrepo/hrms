# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.models import exit_details_model
from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from app.models.exit_details_model import Exit_Employee_Detail
from app.models.employee_model import Employee
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.Exit_DetailsForm import Exit_EmployeeForm
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
import MySQLdb
from itertools import chain
import datetime
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.utils import timezone
import os
from django.core.files.storage import FileSystemStorage




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


def exit_details(request):
   # return HttpResponse("employee")
    employee = Exit_Employee_Detail.objects.filter(is_active='1')
   # return HttpResponse(employee)
    print(employee)
    context = {'employees':employee}
    return render(request, "exit_details/index.html", context)


def snippets_exit_employee_all_info(request):
    
    emp_id =    request.POST.get('emp_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
   
    final_list = Exit_Employee_Detail.objects.filter(employee_id = emp_id)
   
    jsondata = serializers.serialize('json', final_list)
 
    return HttpResponse(jsondata, content_type='application/json')
  


def add_exit_details(request):  
   # return render(request, "exit_details/add_exit_details.html")
    form = Exit_EmployeeForm()
    #return HttpResponse(request.method)
   # """
    if request.method == 'POST':
        form = Exit_EmployeeForm(request.POST)
        if  form.is_valid():
           
            employee = request.POST.get('employee')
           
           
           # Interviewer = request.POST.get('Interviewer')
            reason_leaving = request.POST.get('reason_leaving')
          #  return HttpResponse(employee)
            rejoin_again = request.POST.get('rejoin_again')
            
            like_organi = request.POST.get('like_organi')
            
            vehicle_handled = request.POST.get('vehicle_handled')
            equip_handled = request.POST.get('equip_handled')
           
            improve_staff_welfare = request.POST.get('improve_staff_welfare')
            share_with_us = request.POST.get('share_with_us')
           
            library_book_submit = request.POST.get('library_book_submit')

            security = request.POST.get('security')
            
            exit_interv_conduct = request.POST.get('exit_interv_conduct')
            notice_period_follow = request.POST.get('notice_period_follow')
            resignation_letter = request.POST.get('resignation_letter')
            manager_clearance = request.POST.get('manager_clearance')
           
            seperation_date = request.POST.get('seperation_date')
            if seperation_date != "":
               #return HttpResponse(date)   
               d = datetime.datetime.strptime(seperation_date, '%d-%m-%Y')
               seperation_date = d.strftime('%Y-%m-%d')
            else:
               seperation_date = None    
            
            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            if not Exit_Employee_Detail.objects.filter( Q(employee=employee)).exists():
                obj = Exit_Employee_Detail.objects.create( seperation_date=seperation_date, 
               # Interviewer=Interviewer,
                employee_id=employee, 
                 reason_leaving=reason_leaving, 
                rejoin_again=rejoin_again,
                like_organi=like_organi,

                improve_staff_welfare=improve_staff_welfare,

                share_with_us=share_with_us,
                vehicle_handled=vehicle_handled, 
                equip_handled=equip_handled,
                library_book_submit=library_book_submit,
                security=security,
                exit_interv_conduct=exit_interv_conduct,
                notice_period_follow=notice_period_follow,
               
                resignation_letter=resignation_letter,
                manager_clearance=manager_clearance,
                
                created_at=created_at, updated_at=updated_at, is_active=is_active,

                ) 
               # return HttpResponse(employee)   
                obj.save()
                messages.success(request, 'Employee exit details was added ! ')
                return redirect('exit_details') 
            else: 
                employee = Employee.objects.all()
                context_role = {
                        'employees': employee,
                     
                        }
          
                context_role.update({"form":form})  
                messages.error(request, ' Employee Already Exists! ', context_role)
                context = {'form':form}
                return render(request, "exit_details/add_exit_details.html", context)
                
           
    employee = Employee.objects.all()
    context_role = {
          'employees': employee,
         #  'country': 'in'
       }
   
    #
   # tes = Group.objects.all()
    context_role.update({"form":form})
    print(context_role)
    return render(request, "exit_details/add_exit_details.html",  context_role )
   


def delete_employee_exit_details(request, pk):
   # return HttpResponse('working..')
    data = Exit_Employee_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'Employee exit details was deleted! ')
    return redirect('exit_details')