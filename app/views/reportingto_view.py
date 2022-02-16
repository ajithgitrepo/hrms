
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from app.forms.ReportingToForm import ReportForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm  

from app.models.reporting_to_model import Reporting 
from django.contrib.auth.models import Group
from app.views.restriction_view import admin_only,role_name
from app.models.employee_model import Employee
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.models import Group
from django.db.models import Q


@login_required(login_url="/login/")
#@admin_only
def reporting_to(request):
    #return HttpResponse('work')
    report = Reporting.objects.all()  #filter(is_active='1')
    #return HttpResponse(report);
    context = {'reportings':report}
    return render(request, "reporting_to/index.html", context)

# @admin_only
def add_reporting_to(request):
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
           
            emp_id = request.POST.get('employee')
            rep_id = request.POST.get('reporting')
           # return HttpResponse(rep_id)
            device = "web"
            update_by = request.user.emp_id
            # print(form.errors)
            # print(role_name) 
            if not Reporting.objects.filter(Q(employee_id=emp_id, reporting=rep_id, is_active=1)).exists():
             if Reporting.objects.filter(Q(employee_id=emp_id)).exists():   
              updat = Reporting.objects.filter(employee_id=emp_id).update( is_active= 0, updated_at=timezone.now())   
             ins = Reporting.objects.create(employee_id=emp_id, reporting_id=rep_id, 
             device=device,updated_by_id=update_by)
             messages.success(request,'Reporting was created!')
             return redirect('reporting_to')
            else:
              messages.error(request,'Already Exists!')   

    
    data1 = emp_res_data(request)
    data2 = rep_res_data(request) 
   # return HttpResponse(data)
    context = {'form':form, 'employees': data1, 'reportings': data2 }
    return render(request, "reporting_to/add_repoting_to.html", context)

def emp_res_data(request):                                                          

    emp_roles = Group.objects.filter(is_active='1',name='Associate').values_list('id')
    employee = Employee.objects.filter(is_active='1',role_id__in=emp_roles)
    
    return employee 

def rep_res_data(request):                                                          

    manager_roles = Group.objects.filter(is_active='1',name='manager').values_list('id')
    report_to = Employee.objects.filter(is_active='1', role_id__in=manager_roles)
    
    return report_to        



#@admin_only
def delete_reportingto(request, pk):
    # return HttpResponse('working..')
    data = Reporting.objects.get(id=pk)
    data.is_active = 0
    data.save() 
    messages.success(request, 'reporting_to detail was deleted! ')
    return redirect('reporting_to')


def status_reporting_employee(request,emp_id, pk, val):

    if Reporting.objects.filter(Q(employee_id=emp_id)).exists():   
        updat = Reporting.objects.filter(employee_id=emp_id).update( is_active= 0, updated_at=timezone.now()) 

    # return HttpResponse(val)
    data = Reporting.objects.get(id=pk)
    data.is_active = val
    data.save()

    messages.success(request, 'reporting_to detail status was changed! ')
    return redirect('reporting_to')

def filter_reporting_employees(request,status):
   
    val = [1]
    if(status == "all"):
      val = [1,0]
    if(status == "act"):
     val = [1]
    if(status == "inact"):
     val = [0]
    
    rept = Reporting.objects.filter(is_active__in = val)
  
    context = {'reportings':rept}
    return render(request, "reporting_to/index.html", context)    