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
from datetime import datetime, timedelta


from django.core import serializers
from django.http import JsonResponse
from app.models.leave_balance_model import Leave_Balance
#from app.forms import UserGroupForm  

from app.models.leave_request_model import LeaveRequest 
from app.models.employee_model import Employee 
# from app.models import Group 

from django.contrib.auth.models import Group
from django.db.models import Max, Subquery, OuterRef
from app.models.leave_type_model import * 
from app.models.attendance_model import Attendance
from django.db.models import F
from app.models.leave_type_model import Leave_Type, Leave_Effective, Leave_Applicable, Leave_Restrictions
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage


def leave_request(request):
   
    leave_request = LeaveRequest.objects.filter(is_active='1').annotate(name=Subquery(Employee.objects.filter(employee_id =OuterRef('employee_id')).values('first_name'))).order_by('created_at').reverse()
#     LeaveRequest.objects.filter(competition_id=_competition.id).filter(team_id__in=joined_team_ids).annotate(name=Subquery(Team.objects.filter(id=OuterRef('team_id')).values('name')))
    # print(leave_request)
    context = {'leave_request':leave_request}
    return render(request, "leave_request/index.html", context)

def leave_request_more_info(request):
    
   # roles = Group.objects.def
   # filter(is_active='1')
    id =    request.POST.get('id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
    LeaveReq = LeaveRequest.objects.filter(id = id) #.prefetch_related('id')
    #roles = Group.objects.filter(is_active='1') 
     
    #final_list = Employee.objects.filter(roles).values_list('name', flat=True)
    #final_list =  Employee.objects.raw('select * from auth_group where  id = 3')
    #final_list = Employee.objects.all().prefetch_related(Prefetch('id', queryset=Group.objects.filter(is_active='1')))
    print(LeaveReq)
    jsondata = serializers.serialize('json', LeaveReq)
    
    return HttpResponse(jsondata, content_type='application/json')

def add_leave_request(request):
    #return HttpResponse(request.POST.get('leave_type'))
    form = LeaveRequestForm()
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            
            for each in Leave_Type.objects.filter(is_active='1'):
                leave_type = each.type
                leave_name = each.name
                leave_unit = each.unit
                leave_id = each.id
                for each_restrict in Leave_Restrictions.objects.filter(is_active='1', leave_type_id=leave_id):
                    weekend_bw_leave = each_restrict.weekend_bw_leave
                    weekend_bw_leave_days = each_restrict.weekend_bw_leave_days
                    holydays_bw_leave = each_restrict.holydays_bw_leave
                    holydays_bw_leave_days = each_restrict.holydays_bw_leave_days
                    exceeds_leave_balance = each_restrict.exceeds_leave_balance
                    duration = each_restrict.duration
                    allow_users_to_view = each_restrict.allow_users_to_view
                    balance_to_display = each_restrict.balance_to_display
                    minimum_leave_apply = each_restrict.minimum_leave_apply #
                    maximum_leave_apply = each_restrict.maximum_leave_apply #
                    maximum_consecutive_leave_apply = each_restrict.maximum_consecutive_leave_apply #
                    minimum_gap_apply = each_restrict.minimum_gap_apply #
                    leave_cannot_taken_with = each_restrict.leave_cannot_taken_with #
                    leave_only_on = each_restrict.leave_only_on
                    leave_request_apply_check = each_restrict.leave_request_apply_check
                    leave_request_apply_count = each_restrict.leave_request_apply_count
                    leave_request_future_days = each_restrict.leave_request_future_days
                    leave_request_next_check = each_restrict.leave_request_next_check
                    leave_request_next_count = each_restrict.leave_request_next_count
                    leave_request_past_days = each_restrict.leave_request_past_days
                    maximum_application_period = each_restrict.maximum_application_period
                    past_days_check = each_restrict.past_days_check
                    past_days_count = each_restrict.past_days_count
                    file_upload_after = each_restrict.file_upload_after

            Photo_name = ""
           
            if request.FILES:
                
                upload = request.FILES['document_url']
            
                if upload != None: 
                    logoRoot = os.path.join(settings.MEDIA_ROOT, 'leave_documents/')
                
                    #logo_url = os.path.join(settings.MEDIA_URL, 'profile_images/')
                    logoRoot=logoRoot.replace("\\","/")
                    Photo_name = upload.name
                # return HttpResponse(upload.name) 
                    fs = FileSystemStorage(location=logoRoot)
                    file_name = fs.save(upload.name, upload)
                    file_url = fs.url(file_name)   
                    #return HttpResponse(file_url) 
            #return HttpResponse(Photo_name)             

            employee_id  = request.POST.get('employee')
           # return HttpResponse(employee_id)
            leave_type = request.POST.get('leave_type')
            # return HttpResponse(leave_type)
            date = request.POST.get('from_date')
            if date != "":
               #return HttpResponse(date)
               d = datetime.strptime(date, '%d-%m-%Y')
               fromdate = d.strftime('%Y-%m-%d')
            else:
               fromdate = None 
            
            total_days1 = '0'
            date = request.POST.get('to_date')
            if date != "":
               
               d = datetime.strptime(date, '%d-%m-%Y')
               todate = d.strftime('%Y-%m-%d')
            else:
               todate = None 
               
            #to_date = request.POST.get('to_date')
            if todate != None and  fromdate != None :
                date_format = "%Y-%m-%d"
                a = datetime.strptime(fromdate, date_format)
                b = datetime.strptime(todate, date_format)
                delta = b - a
                total_days = delta.days + 1
                #return HttpResponse(total_days)
                applic = "not_applic"
                
                message = ""
                if (str(total_days) < str(minimum_leave_apply))   and (minimum_leave_apply != None):
                        # if total_days != 0:
                        message = "Minimum " + minimum_leave_apply  + " leave that can be availed per application";
                        #return HttpResponse(message)
                elif (message == "") and (maximum_leave_apply != None):
                        if(int(total_days) >  int(maximum_leave_apply)):
                            message = "Maximum " + maximum_leave_apply  + " leave that can be availed per application";
                elif (message == "") and (maximum_consecutive_leave_apply != None):
                        if(int(total_days) > int(maximum_consecutive_leave_apply)):
                            message = "Maximum " + maximum_consecutive_leave_apply  + "  number of consecutive days of Leave allowed";
                elif  minimum_gap_apply != None:
                    applic = "ok"
                        #return HttpResponse(applic)
                       
                    last_applied =  LeaveRequest.objects.filter(employee_id=employee_id).order_by('from_date').reverse()
                    #return HttpResponse(last_applied)
                    last_leave_d = 0
                    if last_applied != None and  len(last_applied) < 0:
                            last_applied_leave_date = last_applied[0].from_date
                            #return HttpResponse('it works')
                            date_format = "%Y-%m-%d"
                            last_leave_d = (str(last_applied_leave_date))
                    
                            #datetime.now().strftime("%Y-%m-%d")
                    
                            datetime_object = datetime.strptime(last_leave_d, '%Y-%m-%d').date()
                    
                            datetime_object1 = datetime.strptime(fromdate, '%Y-%m-%d').date()
                            #return HttpResponse(datetime_object1)
                            # datetime.strptime(last_leave_d, '%Y-%m-%d').date()
                            
                            delta = datetime_object1 - datetime_object
                    
                            total_days1 = delta.days
                       # return HttpResponse(total_days) 
                       
                            if(int(minimum_gap_apply) >= int(total_days1)):
                                applic = "ok" 
                                message = "Require minimum " + minimum_gap_apply + " days gap  between two applications ! "
                                #return HttpResponse(applic)
                                    #messages.error(request, message)
                                    #return redirect('leave_request')
                                    #return HttpResponse(1)
                              

                    if message != "":
                        employee = Employee.objects.filter(is_active='1')
                        messages.error(request, message)
                        leave_type =  Leave_Type.objects.filter(is_active='1')
    
                        context_role = { 
                              'employees': employee, 'form':form,  'leaves': leave_type,} 
                        return render(request, "leave_request/add_leave_request.html", context_role)
                        # return HttpResponse(applic)
                  # return HttpResponse(total_days)
                  # if leave_cannot_taken_with == "1":
                  #       applic = "ok"                        
             
            #return HttpResponse(total_days)
            
            team_mailid = request.POST.get('team_mailid')
            reason = request.POST.get('reason')
            is_approved = '0'
            is_rejected = '0'
            added_by = 'admin'
            is_active = '1'
            device = 'web'
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # print(form.errors)
            # print(role_name)
            g1 = LeaveRequest.objects.create(
                employee=Employee.objects.get(employee_id = employee_id) if employee_id else None,
                leave_type=Leave_Type.objects.get(id = leave_type) if leave_type else None, 
                from_date=fromdate, 
                to_date=todate, 
                total_days=total_days, 
                team_mailid=team_mailid, 
                reason=reason,
                is_approved=is_approved, 
                is_rejected=is_rejected, 
                added_by=Employee.objects.get(employee_id = request.user.emp_id) if request.user.emp_id else None, 
                is_active=is_active, 
                device=device, 
                created_at=created_at, 
                updated_at=updated_at,
                document_url=Photo_name,
                
            )
            messages.success(request,'Leave request send successfully ! ')
            return redirect('leave_request')
    # print(form.errors)
    context = {'form':form}
    employee = Employee.objects.filter(is_active='1')
    leave_type =  Leave_Type.objects.filter(is_active='1')
    context_role = {
           # 'employees': employee,
             'employees': employee, 'form':form,  'leaves': leave_type,} 
           #}
    #context_role.update({"form":form, 'employee':employee})
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
            g1 = LeaveRequest.objects.filter(id=pk).update(
                employee_id=employee_id, 
                leave_type=leave_type, 
                from_date=fromdate, 
                to_date=todate, 
                total_days=total_days, 
                team_mailid=team_mailid, 
                reason=reason,
                updated_at=updated_at
            )

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


def change_leave_status(request):

    id = request.POST.get('id')
    value = request.POST.get('value')

    data = LeaveRequest.objects.get(id = id)

    update = LeaveRequest.objects.filter(id=id).update(
        is_approved=value, 
        # is_rejected=value, 
        action_by_id=request.user.emp_id, 
        updated_by_id = request.user.emp_id,
        updated_at=timezone.now()
    )

    if update:
        start_date = datetime.strptime(str(data.from_date), "%Y-%m-%d")
        end_date = datetime.strptime(str(data.to_date), "%Y-%m-%d")
        diff = abs((end_date-start_date).days)+1

        delta = end_date - start_date
        # print(value)
        first = True
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            # print(datetime.strftime(day, "%d-%m-%Y"))
            
            if value == '1':
                attn = Attendance.objects.filter(date=datetime.strftime(day, "%Y-%m-%d"), employee_id= data.employee_id).update(
                    is_leave_approved=1, 
                    leave_approved_by_id = request.user.emp_id,
                    updated_at=timezone.now()
                )
                if first:
                    first = False
                    decr = Leave_Balance.objects.filter(employee_id=data.employee_id, leave_type_id=data.leave_type_id ).update(
                        balance=F('balance') - diff,
                        updated_at=timezone.now()
                    )

            if value == '0' or value == '2':
                attn = Attendance.objects.filter(date=datetime.strftime(day, "%Y-%m-%d"), employee_id= data.employee_id).update(
                    is_leave_approved=0, 
                    leave_approved_by_id = None,
                    updated_at=timezone.now()
                )

        return HttpResponse(1)
    return HttpResponse(0)