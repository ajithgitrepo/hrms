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
from app.forms.LeaveRequestForm import LeaveRequestForm
from django.utils import timezone
import datetime 
from datetime import datetime
from django.core import serializers
from django.http import JsonResponse
#from app.forms import UserGroupForm  

from app.models.leave_request_model import LeaveRequest 
from app.models.employee_model import Employee 
# from app.models import Group 

from django.contrib.auth.models import Group
from django.db.models import Max, Subquery, OuterRef



# @login_required(login_url="/login/")
# def index(request):
    
#     context = {}
#     context['segment'] = 'index' 

#     html_template = loader.get_template( 'index.html' )
#     return HttpResponse(html_template.render(context, request))


# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:
        
#         load_template      = request.path.split('/')[-1]
#         context['segment'] = load_template
        
#         html_template = loader.get_template( load_template )
#         return HttpResponse(html_template.render(context, request))
        
#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template( 'page-404.html' )
#         return HttpResponse(html_template.render(context, request))

#     except:
    
#         html_template = loader.get_template( 'page-500.html' )
#         return HttpResponse(html_template.render(context, request))

def leave_request(request):
    print('it works')
    
    #return HttpResponse('works')
    leave_request = LeaveRequest.objects.filter(is_active='1').annotate(name=Subquery(Employee.objects.filter(employee_id =OuterRef('employee_id')).values('first_name')))
#     LeaveRequest.objects.filter(competition_id=_competition.id).filter(team_id__in=joined_team_ids).annotate(name=Subquery(Team.objects.filter(id=OuterRef('team_id')).values('name')))
    print(leave_request);
    #return HttpResponse(leave_request)
    context = {'leave_request':leave_request}
    return render(request, "leave_request/index.html", context)

def leave_request_more_info(request):
    
   # roles = Group.objects.filter(is_active='1')
    id =    request.POST.get('id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
    LeaveReq = LeaveRequest.objects.filter(id = id) #.prefetch_related('id')
    #roles = Group.objects.filter(is_active='1') 
     
    #final_list = Employee.objects.filter(roles).values_list('name', flat=True)
    #final_list =  Employee.objects.raw('select * from auth_group where  id = 3')
    #final_list = Employee.objects.all().prefetch_related(Prefetch('id', queryset=Group.objects.filter(is_active='1')))
    #print(final_list)
    jsondata = serializers.serialize('json', LeaveReq)
    
    return HttpResponse(jsondata, content_type='application/json')

def add_leave_request(request):
    #return HttpResponse('it works')
    form = LeaveRequestForm()
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            employee_id  = request.POST.get('employee_id')
            #return HttpResponse(employee_id)
            leave_type = request.POST.get('leave_type')
           # todate = request.POST.get('todate')
            date = request.POST.get('from_date')
            if date != "":
               #return HttpResponse(date)
               d = datetime.strptime(date, '%d-%m-%Y')
               fromdate = d.strftime('%Y-%m-%d')
            else:
               fromdate = None 
            
            total_days = '0'
            date = request.POST.get('to_date')
            if date != "":
               
               d = datetime.strptime(date, '%d-%m-%Y')
               todate = d.strftime('%Y-%m-%d')
            else:
               todate = None 
               
            #to_date = request.POST.get('to_date')
            if todate != "" and  fromdate != "" :
                  date_format = "%Y-%m-%d"
                  a = datetime.strptime(fromdate, date_format)
                  b = datetime.strptime(todate, date_format)
                  delta = b - a
                  total_days = delta.days
             
            #return HttpResponse(total_days)
            
            team_mailid = request.POST.get('team_mailid')
            reason = request.POST.get('reason')
            is_approved = '0'
            is_rejected = '0'
            added_by = 'employee'
            is_active = '1'
            device = 'web'
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # print(form.errors)
            # print(role_name)
            g1 = LeaveRequest.objects.create(employee_id=employee_id, leave_type=leave_type, from_date=fromdate, 
            to_date=todate, total_days=total_days, team_mailid=team_mailid, reason=reason,
            is_approved=is_approved, is_rejected=is_rejected, added_by=added_by,
            is_active=is_active, device=device, created_at=created_at, updated_at=updated_at)
            messages.success(request,'Leave request send successfully ! ')
            return redirect('leave_request')
    # print(form.errors)
    context = {'form':form}
    employee = Employee.objects.filter(is_active='1')
    context_role = {
            'employees': employee,
           }
    context_role.update({"form":form, 'employee':employee})
    #return HttpResponse(employee)
    return render(request, "leave_request/add_leave_request.html", context_role)

def update_leave_request(request, pk):
    leave_request = LeaveRequest.objects.get(id=pk)
    form = LeaveRequestForm(instance=leave_request)
    # print(role)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave_request)
        if form.is_valid():
            employee_id  = request.POST.get('employee_id')
            #return HttpResponse(employee_id)
            leave_type = request.POST.get('leave_type')
           # todate = request.POST.get('todate')
            date = request.POST.get('from_date')
            if date != "":
               #return HttpResponse(date)
               d = datetime.strptime(date, '%d-%m-%Y')
               fromdate = d.strftime('%Y-%m-%d')
            else:
               fromdate = None 
            
            total_days = '0'
            date = request.POST.get('to_date')
            if date != "":
               
               d = datetime.strptime(date, '%d-%m-%Y')
               todate = d.strftime('%Y-%m-%d')
            else:
               todate = None 
               
            #to_date = request.POST.get('to_date')
            if todate != "" and  fromdate != "" :
                  date_format = "%Y-%m-%d"
                  a = datetime.strptime(fromdate, date_format)
                  b = datetime.strptime(todate, date_format)
                  delta = b - a
                  total_days = delta.days
             
            #return HttpResponse(total_days)
            
            team_mailid = request.POST.get('team_mailid')
            reason = request.POST.get('reason')
            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # print(form.errors)
            # print(role_name)
            g1 = LeaveRequest.objects.filter(id=pk).update(employee_id=employee_id, leave_type=leave_type, from_date=fromdate, 
            to_date=todate, total_days=total_days, team_mailid=team_mailid, reason=reason,
            
            updated_at=updated_at)
            leave_request.updated_at = timezone.now()
            leave_request.save()
           
            messages.success(request, ' Leave Request was updated! ')
            return redirect('leave_request')
    context = {'form':form,'leave_request':leave_request}
    return render(request, "leave_request/update_leave_request.html", context)

def delete_leave_request(request, pk):
    # return HttpResponse('working..')
    data = LeaveRequest.objects.get(id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, ' Request was deleted! ')
    return redirect('leave_request')