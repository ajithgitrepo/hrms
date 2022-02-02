
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
from app.views.employee_view import employees, reporting
from app.views.location_view import locations
from app.views.restriction_view import admin_only,role_name
from app.models.employee_model import Employee
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.models import Group
from django.db.models import Q
from app.models.department_model import Department
from app.models.location_model import Location
from django.db.models import Prefetch
from pprint import pprint
from django.core import serializers
from django.db import connection
from django.http import JsonResponse


@login_required(login_url="/login/")
#@admin_only
def emp_mapping(request):
    #return HttpResponse('work')
    # emp = Employee.objects.all().annotate(test=Subquery(Reporting.objects.filter(employee = OuterRef('reporting_to_employee')).values('reporting_id')))
    # return HttpResponse(emp.query)
    #
    #.prefetch_related(Prefetch('reporting_to_employee', queryset=Reporting.objects.filter(is_active = '1')))
    #Employee.objects.filter(is_active='1').select_related('role')
    #.annotate(test=Subquery(Reporting.objects.filter(reporting = OuterRef('report_employee')).values('reporting_id')))
    #return HttpResponse(emp);
  #  pprint(vars(emp))
  
     cursor = connection.cursor()
     cursor.execute("SELECT `emp`.`employee_id`, `emp`.`first_name`, `emp`.`last_name`, `rl`.`name` as role,  `dt`.`name`, `lc`.`location` as location , `rt`.`reporting_id` as rpt_emp, (SELECT CONCAT(first_name, ' ' ,last_name) FROM `employee`  WHERE  employee_id = rt.reporting_id) AS `test` FROM employee emp LEFT JOIN reporting_to rt ON emp.employee_id = rt.employee_id LEFT JOIN department dt ON emp.department_id = dt.id LEFT JOIN auth_group rl ON emp.role_id = rl.id LEFT JOIN location lc ON emp.location_id = lc.id  WHERE rt.is_active='1' and emp.is_active= '1'")
     objs = cursor.fetchall()
     json_data = []
     for obj in objs:
      json_data.append({"employee_id" : obj[0], "first_name" : obj[1], "last_name" : obj[2], "role" : obj[3], "department" : obj[4], "location" : obj[5] , "rpt_emp" : obj[6], "test" : obj[7]})
    # return JsonResponse(json_data, safe=False)
     context = {'employees':json_data }
     return render(request, "emp_mapping/index.html", context)


# @admin_only
def add_emp_mapping(request,pk):
    
    if request.method == 'POST':
        emp_id = request.POST.get('employee')
        dept_id = request.POST.get('department')
        role_id = request.POST.get('role')
        loc_id = request.POST.get('location')
        rep_id = request.POST.get('reporting')
        if emp_id != None and (dept_id != None or role_id != None or loc_id != None or rep_id != None) :
           
            updat = Employee.objects.filter(employee_id=emp_id).update( 
                  department= dept_id, role = role_id, location = loc_id,reporting = rep_id,
                 updated_at=timezone.now())   
            if emp_id != None:
              if not Reporting.objects.filter(Q(employee_id=emp_id, reporting=rep_id, is_active=1)).exists():
               if Reporting.objects.filter(Q(employee_id=emp_id)).exists():   
                  updat = Reporting.objects.filter(employee_id=emp_id).update( is_active= 0, updated_at=timezone.now())   
              ins = Reporting.objects.create(employee_id=emp_id, reporting_id=rep_id, 
              device="web",updated_by_id=request.user.emp_id)
            messages.success(request,'Details was created!')
            return redirect('emp_mapping') 
             
    
    role = Group.objects.filter(is_active=1)
    department = Department.objects.filter(is_active=1)
    loc = Location.objects.filter(is_active=1)
    emp = Employee.objects.filter(is_active=1)
#     reporting = Employee.objects.filter(
#         is_active=1).exclude(employee_id=request.user.emp_id)  
   # return HttpResponse(data)
    context = {'roles': role,
       # 'reporting': reporting,
        'department': department,
        'location': loc,
        'employees': emp }
    return render(request, "emp_mapping/add_emp_mapping.html", context)

     



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