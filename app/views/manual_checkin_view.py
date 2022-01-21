

#from app.models import compensatory_request_model
#from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from app.models.manual_checkin_model import Manual_Checkin_Detail
from app.models.employee_model import Employee
from django.contrib.auth.decorators import login_required
#from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
#from django.http import HttpResponseRedirect
from app.forms.ManualChekinForm import ManualChekinForm
from django.conf import settings
from app.views.restriction_view import admin_only,role_name
from app.models.attendance_model import Attendance 

#from app.models import Group 
from django.conf.urls import url
#from pprint import pprint
from django.shortcuts import render
# from django.template import RequestContext
from django.db.models import Q
from datetime import datetime

from app.models.reporting_to_model import Reporting 
# from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection

import datetime

from django.utils import timezone



@login_required(login_url="/login/")
def manual_checkin_details(request):
   
    employee = Manual_Checkin_Detail.objects.filter(is_active='1').order_by('-created_at')
    context = {'employees':employee}
    return render(request, "manual_checkin_details/index.html", context)


def snippets_compensatory_details_employee_all_info(request):
    
    id =    request.POST.get('emp_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
   
    final_list = Manual_Checkin_Detail.objects.filter(id = id)
    # print(final_list)
    jsondata = serializers.serialize('json', final_list)
 
    return HttpResponse(jsondata, content_type='application/json')
  


def add_manual_checkin_details(request):  
    #return HttpResponse('wewe')
    form = ManualChekinForm()
    
    if request.method == 'POST':
        form = ManualChekinForm(request.POST)
        if  form.is_valid():
            #return HttpResponse('wewe')   
            employee = request.POST.get('employee')
            
            worked_date = request.POST.get('worked_date')
            if worked_date != "" and worked_date != None:
               d = datetime.datetime.strptime(worked_date, '%d-%m-%Y')
               worked_date = d.strftime('%Y-%m-%d')
            else:
               worked_date = None  


            ftime = request.POST.get('clockpicker_one')
            from_time = datetime.datetime.strptime(ftime, '%H:%M:%S')
            
            ttime = request.POST.get('clockpicker_two')
            to_time = datetime.datetime.strptime(ttime, '%H:%M:%S')
            #return HttpResponse(ttime) 
            reason = request.POST.get('reason')

            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            created = str(worked_date) + " " + str(ftime)
            updated = str(worked_date) + " " + str(ttime)

            #return HttpResponse(updated)
            # if not Asset_Detail.objects.filter( Q(employee=employee)).exists():
            obj = Manual_Checkin_Detail.objects.create( 

                  employee_id=employee, 
                  worked_date=worked_date,
                  from_time=from_time,to_time=to_time,
                  reason=reason,created_by_id=request.user.emp_id,
                  created_at=created_at, 
                  updated_at=updated_at, 
                  is_active=is_active,
            ) 
            obj.save()

            if not Attendance.objects.filter(Q(employee_id=employee, date=worked_date, checkin_time__isnull=False)).exists():
                insert = Attendance.objects.create(date=worked_date, 
                checkin_time=from_time, employee_id= employee, 
                checkout_time = to_time,is_present = 1,
                last_checkout = updated, 
                first_checkin=created,
            )

            #     update1 = Attendance.objects.filter(date=worked_date, employee_id = employee ).update(
            #     updated_at = updated, 
            #     created_at=created
            # )
            else:
                update = Attendance.objects.filter(date=worked_date, employee_id = employee ).update(
                checkin_time=from_time, 
                checkout_time = to_time,
                updated_at = updated, 
                employee_id= employee)

            messages.success(request, 'Checked details was added ! ')
            return redirect('manual_checkin_details') 
    
    employee1 = Employee.objects.filter(is_active='1')
        # print(employee)

    context_role = {
          'employees': employee1,
       }
   
    #
   # tes = Group.objects.all()
    context_role.update({"form":form})
    #return HttpResponse('wewe4')
    return render(request, "manual_checkin_details/add_manual_checkin_details.html",  context_role )
   
def delete_manual_check_details(request, pk):
   # return HttpResponse('working..')
   
    data = Manual_Checkin_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'checkin details was deleted! ')
    return redirect('manual_checkin_details')

