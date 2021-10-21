# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.models import Calendar_Detail
from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from app.models.calendar_model import Calendar_Detail 
from app.models.holiday_details_model import Holiday_Detail 

from app.models.holiday_details_model import Holiday_Detail 
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
# from app.forms.Holiday_DetailsForm import Holiday_DetailsForm
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
from datetime import date, timedelta

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

def calendar(request):
   # return HttpResponse('work')  
    all_events = Calendar_Detail.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'calendar_details/calendar.html',context)

def all_events(request):   
    #return HttpResponse('work')  
                                                                                                    
    all_events = Calendar_Detail.objects.all() 
    all_holidays = Holiday_Detail.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
            'end': event.end.strftime("%m/%d/%Y"),  
            'color': '#7f7fff',                                                           
        })  
    for holi in all_holidays:                                                                                             
        out.append({                                                                                                     
            'title': holi.holiday_name,                                                                                         
            'id': holi.id,                                                                                              
            'start': holi.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
            'end': holi.date.strftime("%m/%d/%Y"),  
            'color': '#ff1a1a',                                                           
        })                                                                                                                    
    #return HttpResponse(out)                                                                                                                   
    return JsonResponse(out, safe=False)  

def add_event(request):
   # return HttpResponse('work')    
    csrf =    request.POST.get('csrfmiddlewaretoken')    
    start = request.POST.get("start")
    end = request.POST.get("end")
    title = request.POST.get("title")
    event = Calendar_Detail(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data, content_type='application/json')


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Calendar_Detail.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
   # return JsonResponse('data')  
    csrf =    request.POST.get('csrfmiddlewaretoken')   
    id = request.POST.get("id")
    event = Calendar_Detail.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data, content_type='application/json')

# def holiday_details(request):
   
#     employee = Holiday_Detail.objects.filter(is_active='1')
# #     Asset_Detail.objects.select_related('employee').get(is_active='1')
#     print(employee)
#     context = {'employees':employee}
#     return render(request, "holiday_details/index.html", context)


