
from app.models import exit_details_model
from app.models import leave_type_model
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
from app.forms.ApplyLeaveForm import Apply_Leave_Form
from django.conf import settings
from app.models.holiday_details_model import Holiday_Detail
from app.models.weekend_model import Weekend
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.models import Group
from app.models.attendance_model import Attendance
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
from datetime import date, time, datetime, timedelta
import calendar
from django.utils import timezone
from app.forms.EmployeeFilesForm import Employee_Files_Form
from app.models.folder_model import Folder
from app.models.leave_balance_model import Leave_Balance
from django.views import generic
from app.models.employee_files_model import Employee_Files
from app.models.leave_type_model import *
from app.models.leave_request_model import *
import os
from django.db.models import Avg, Count, Min, Sum, Case, When, F


@login_required(login_url="/login/")
def profile(request):

    employee = Employee.objects.select_related().get(
        is_active='1', employee_id=request.user.emp_id)
    # print(employee.department.name)
    context = {'employee': employee}

    return render(request, "self_service/profile.html", context)


def attendance(request):

    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    month_year = current_month+'-'+current_year
    first_day = now.replace(day=1)
    last_day = now.replace(day=calendar.monthrange(now.year, now.month)[1])
    # no_of_days = calendar.monthrange(current_year, current_month )

    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append((first_day + timedelta(days=i)))
        date_no.append((first_day + timedelta(days=i)).strftime("%d"))

    # print(dates)

    month_atten = Attendance.objects.filter(
        is_active=1, employee_id=request.user.emp_id, date__range=[first_day, last_day])
    # print(month_atten)

    present_days = Attendance.objects.filter(
        is_active=1, is_present=1, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(present_days)

    absent_days = Attendance.objects.filter(
        is_active=1, is_leave=1, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(absent_days)

    zipped_data = zip(dates, date_no)
    # print(date_no)
    employees = Employee.objects.filter(is_active=1)

    holidays = Holiday_Detail.objects.filter(
        is_active=1, date__range=[first_day, last_day])

    weekend = Weekend.objects.filter(is_active=1)
    # print(weekend)

    num_days = len([1 for i in calendar.monthcalendar(
        datetime.now().year, datetime.now().month) if i[6] != 0])

    context = {
        'month_atten': month_atten,
        'holidays': holidays,
        'zipped_data': zipped_data,
        'employees': employees,
        'present_days': present_days,
        'absent_days': absent_days,
        'month': now.strftime("%b"),
        'month_no': now.strftime("%m"),
        'year': now.strftime("%Y"),
        'emp_id': request.user.emp_id,
        'weekend': weekend,
        'weekend_count': num_days,

    }

    return render(request, "self_service/attendance.html", context)


def filter_attendance(request, month):

    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    # first_day = now.replace(day = 1)
    # last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])
    # no_of_days = calendar.monthrange(current_year, current_month )
    date = datetime.strptime(month, "%m-%Y")
    first_day = date.replace(day=1)
    last_day = date.replace(day=calendar.monthrange(date.year, date.month)[1])
    # print(date.strftime("%Y"))

    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append((first_day + timedelta(days=i)))
        date_no.append((first_day + timedelta(days=i)).strftime("%d"))

    month_atten = Attendance.objects.filter(
        is_active=1,  employee_id=request.user.emp_id, date__range=[first_day, last_day])
    # print(month_atten)

    zipped_data = zip(dates, date_no)
#    print(zipped_data)
    employees = Employee.objects.filter(is_active=1)

    present_days = Attendance.objects.filter(
        is_active=1, is_present=1, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(present_days)

    absent_days = Attendance.objects.filter(
        is_active=1, is_leave=1, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(absent_days)

    holidays = Holiday_Detail.objects.filter(
        is_active=1, date__range=[first_day, last_day])

    weekend = Weekend.objects.filter(is_active=1)
    # print(weekend)

    num_days = len([1 for i in calendar.monthcalendar(
        datetime.now().year, datetime.now().month) if i[6] != 0])

    context = {
        'month_atten': month_atten,
        'holidays': holidays,
        'zipped_data': zipped_data,
        'employees': employees,
        'present_days': present_days,
        'absent_days': absent_days,
        'search_id': request.user.emp_id,
        'month': date.strftime("%b"),
        'month_no': date.strftime("%m"),
        'year': date.strftime("%Y"),
        'emp_id': request.user.emp_id,
        'weekend': weekend,
        'weekend_count': num_days,
    }

    return render(request, "self_service/attendance.html", context)

def files(request):
    
    queryset = Employee_Files.objects.filter(is_active = 1, employee__is_active = 1, employee_id = request.user.emp_id)
    # folders = Employee_Files.objects.filter(is_active = 1, employee_id = request.user.emp_id).values_list('folder').annotate(count=Count('folder')).order_by('folder')
    
    folders = (Employee_Files.objects.filter(is_active = 1, employee_id = request.user.emp_id).values('folder').annotate(dcount=Count('folder')).order_by('folder'))
    

    context = {
        'files': queryset,
        'folders': folders,

    }
    return render(request, "self_service/files.html", context)


def add_files(request):  

    form = Employee_Files_Form()


    if request.method == 'POST':
        form = Employee_Files_Form(request.POST, request.FILES)

        if form.is_valid():
            
            current_date_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  
            handle_uploaded_file(request.FILES['file'], request.POST.get('name'), request.POST.get('folder'), current_date_time)
            extesion = os.path.splitext(str(request.FILES['file']))[1]
            if request.POST.get('date_until'):
                date = datetime.strptime(request.POST.get('date_until'), "%d-%m-%Y")
                db_date = date.strftime('%Y-%m-%d')
            else:
                db_date = None
            

            obj = Employee_Files.objects.create( 
                file = request.POST.get('name')+"-"+current_date_time+""+extesion,
                name = request.POST.get('name'),
                description = request.POST.get('description'),
                device = 'web',
                employee_id= request.user.emp_id,
                added_by_id= request.user.emp_id,
                updated_by_id= request.user.emp_id,
                valid_until= db_date, 
                folder = request.POST.get('folder'),
               
            )

            return redirect('files') 

    folders = Folder.objects.filter(is_active = 1)
   
    context = {
        'form' : form,
        'folders' : folders,
    }

    return render(request, "self_service/add_files.html",  context )


def handle_uploaded_file(f, name, folder, current_date_time):
    
    extesion = os.path.splitext(str(f))[1]
    file_name = name+"-"+current_date_time+""+extesion
    if folder !=None:
        directory = folder
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'files/employee/'+directory), exist_ok=True)
        file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'files/employee/'+directory)

    else:
        file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'files/employee')

    with open(os.path.join(file_upload_dir, file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def assets(request):
    
    assets = Asset_Detail.objects.filter(is_active='1',employee_id = request.user.emp_id)
    context = {
        'assets':assets
    }
    return render(request, "self_service/assets.html", context)



def add_asset(request):  
    form = Asset_DetailForm()
    if request.method == 'POST':
       
        form = Asset_DetailForm(request.POST)
        if  form.is_valid():
            # print('enter')
            employee = request.user.emp_id
           
            type_of_asset = request.POST.get('type_of_asset')
        
            asset_details = request.POST.get('asset_details')
            
            given_date = request.POST.get('given_date')
            if given_date != "":
               #return HttpResponse(date)   
               d = datetime.strptime(given_date, '%d-%m-%Y')
               given_date = d.strftime('%Y-%m-%d')
            else:
               given_date = None  

            return_date = request.POST.get('return_date')
            if return_date != "":
               #return HttpResponse(date)   
               d = datetime.strptime(return_date, '%d-%m-%Y')
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
                created_at=created_at,
                updated_at=updated_at, 
                is_active=is_active,

            ) 
              
            obj.save()
            messages.success(request, 'Asset details was added ! ')
            return redirect('assets') 
       
    employee = Employee.objects.all()
    context_role = {
        'employees': employee,
       
    }
   
    context_role.update({"form":form})
  
    return render(request, "self_service/add_asset.html",  context_role )
   

def leave_tracker(request):

    leaves = Leave_Balance.objects.filter(is_active = 1, leave_type__is_active = 1, employee_id=request.user.emp_id) 
    # print(leaves[0].leave_type.name)

    requested = LeaveRequest.objects.filter(to_date__gte=datetime.now(), employee_id=request.user.emp_id)
    # print(requested)

    all_requestes = LeaveRequest.objects.filter(leave_type__is_active = 1, employee_id=request.user.emp_id).order_by('-created_at')
    # print(all_requestes)




    obj = []
    ids = []
    count = 0

    myDict = {}

    # for index, data in enumerate(requested):
        
    #     if data.leave_type_id in ids:

    #         print(index)
    #         # (obj[data.leave_type_id]['count']) += int(data.total_days)
    #         # print(myDict)
    #         count += int(data.total_days)
    #         # obj.append({'id': data.leave_type_id, 'count': count})
    #     else:
    #         ids.append(data.leave_type_id)
    #         obj.append({int(data.leave_type_id):{'id': data.leave_type_id, 'count': int(data.total_days)}})
    #         # print(obj)
    #         # count = int(data.total_days)
    #         # obj.append({'id': data.leave_type_id, 'count': count})

    # # print(obj)

    context = {
        'leaves': leaves,
        'requested': requested,
        'all_requestes': all_requestes,
    }

    return render(request, "self_service/leave_tracker.html",  context )


def apply_leave(request):
    form = Apply_Leave_Form()
    if request.method == 'POST':
       
        form = Apply_Leave_Form(request.POST)
        if  form.is_valid():
            emp_id = request.POST.get('employee_id')
            leave = request.POST.get('leave_type')
            from_date = datetime.strptime(request.POST.get('from_date'), '%d-%m-%Y')
            to_date = datetime.strptime(request.POST.get('to_date'), '%d-%m-%Y')
            reason = request.POST.get('reason')
            created_at = timezone.now()
            updated_at = timezone.now()

            start_date = datetime.strptime(request.POST.get('from_date'), "%d-%m-%Y")
            end_date = datetime.strptime(request.POST.get('to_date'), "%d-%m-%Y")
            diff = abs((end_date-start_date).days)+1
            # print(diff)

            delta = end_date - start_date       # as timedelta

            obj = LeaveRequest.objects.create( 
                employee_id=Employee.objects.get(employee_id = emp_id) if emp_id else None, 
                leave_type=Leave_Type.objects.get(id = leave) if leave else None,
                from_date=from_date.strftime('%Y-%m-%d'),
                to_date=to_date.strftime('%Y-%m-%d'),
                total_days = diff,
                reason=reason,
                created_at=created_at,
                updated_at=updated_at, 
                is_active=1,
                added_by = Employee.objects.get(employee_id = request.user.emp_id) if request.user.emp_id else None, 
                device = 'web',

            ) 
            obj.save()

            for i in range(delta.days + 1):
                day = start_date + timedelta(days=i)
                # print(datetime.strftime(day, "%d-%m-%Y"))  
                insert = Attendance.objects.create(date=datetime.strftime(day, "%Y-%m-%d"), employee_id= emp_id, is_leave = 1 )

            messages.success(request, 'Leave Requested Successfully ! ')
            return redirect('leave_tracker') 


    employee = Employee.objects.get(is_active = 1, employee_id = request.user.emp_id)
    
    leaves = Leave_Applicable.objects.filter(is_active = 1, leave_type__is_active = 1, all_employees = 1).exclude(exception_dept = employee.department_id, exception_role = employee.role_id, exception_location = employee.location )
    
    leave_condition = Leave_Applicable.objects.filter(is_active = 1, leave_type__is_active = 1, all_employees = 0, gender = employee.gender, marital_status = employee.marital_status, department = employee.department_id, role = employee.role_id, location = employee.location, employment_type = employee.employee_type )
    # print(leaves)

    context = {
        'form' : form,
        'leaves' : leaves,
        'leave_condition':leave_condition,
    }

    return render(request, "self_service/apply_leave.html",  context )

def leave(request,leave):
    path = request.path.split("/")
    print(path[2])
    leave_type=path[2]
    form = Apply_Leave_Form()
    if request.method == 'POST':
        form = Apply_Leave_Form(request.POST)
        if  form.is_valid():
            emp_id = request.POST.get('employee_id')
            leave = request.POST.get('leave_type')
            from_date = datetime.strptime(request.POST.get('from_date'), '%d-%m-%Y')
            to_date = datetime.strptime(request.POST.get('to_date'), '%d-%m-%Y')
            reason = request.POST.get('reason')
            created_at = timezone.now()
            updated_at = timezone.now()
            start_date = datetime.strptime(request.POST.get('from_date'), "%d-%m-%Y")
            end_date = datetime.strptime(request.POST.get('to_date'), "%d-%m-%Y")
            diff = abs((end_date-start_date).days)+1
            # print(diff)
            delta = end_date - start_date       # as timedelta
            obj = LeaveRequest.objects.create(
                employee_id=Employee.objects.get(employee_id = emp_id) if emp_id else None,
                leave_type=Leave_Type.objects.get(id = leave) if leave else None,
                from_date=from_date.strftime('%Y-%m-%d'),
                to_date=to_date.strftime('%Y-%m-%d'),
                total_days = diff,
                reason=reason,
                created_at=created_at,
                updated_at=updated_at,
                is_active=1,
                added_by = Employee.objects.get(employee_id = request.user.emp_id) if request.user.emp_id else None,
                device = 'web',
            )
            obj.save()
            for i in range(delta.days + 1):
                day = start_date + timedelta(days=i)
                # print(datetime.strftime(day, "%d-%m-%Y"))
                insert = Attendance.objects.create(date=datetime.strftime(day, "%Y-%m-%d"), employee_id= emp_id, is_leave = 1 )
            messages.success(request, 'Leave Requested Successfully ! ')
            return redirect('leave_tracker')
    employee = Employee.objects.get(is_active = 1, employee_id = request.user.emp_id)
    leaves = Leave_Applicable.objects.filter(is_active = 1, leave_type__is_active = 1, all_employees = 1).exclude(exception_dept = employee.department_id, exception_role = employee.role_id, exception_location = employee.location )
    leave_condition = Leave_Applicable.objects.filter(is_active = 1, leave_type__is_active = 1, all_employees = 0, gender = employee.gender, marital_status = employee.marital_status, department = employee.department_id, role = employee.role_id, location = employee.location, employment_type = employee.employee_type )
    # print(leaves)
    context = {
        'form' : form,
        'leaves' : leaves,
        'leave_condition':leave_condition,
        'leave_type':leave_type,
    }
    return render(request, "self_service/apply_leave.html",  context )