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
from app.models.travel_expense_model import *
from app.models.reporting_to_model import *
import os
from django.db.models import Avg, Count, Min, Sum, Case, When, F
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from app.models.compensatory_request_model import Compoensatory_Request_Detail
from app.forms.CompensatoryRequest_DetailsForm import CompensatoryRequest_DetailForm
from app.forms.TarvelRequest_DetailsForm import TarvelRequest_DetailForm
from app.models.travel_request_model import Travel_Request_Detail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings

@login_required(login_url="/login/")
def profile(request):

    employee = Employee.objects.select_related().get(is_active='1', employee_id=request.user.emp_id)
    # print(employee.department.name)

    reporting = Reporting.objects.filter(is_active = 1, employee_id = request.user.emp_id, reporting_id__is_active = 1)
    # print(reporting[0].reporting.first_name)
    context = {'employee': employee, 'reporting':reporting}

    return render(request, "self_service/profile.html", context)


def attendance(request):

    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    month_year = current_month+'-'+current_year
    first_day = now.replace(day=1)
    last_day = now.replace(day=calendar.monthrange(now.year, now.month)[1])
    # no_of_days = calendar.monthrange(current_year, current_month )

    myDate = datetime.today()

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

    full_present_days = Attendance.objects.filter(is_active=1, is_present=1, is_half=0, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    
    half_present_days = Attendance.objects.filter(is_active=1, is_present=1, is_half=1, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    
    present_days = full_present_days + (half_present_days * 0.5)
    # print(present_days)

    full_absent_days = Attendance.objects.filter(is_active=1, is_leave=1, is_leave_approved = 1, is_half = 0, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    
    half_absent_days = Attendance.objects.filter(is_active=1, is_leave=1, is_leave_approved = 1, is_half = 1, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
   
    absent_days = full_absent_days + (half_absent_days * 0.5)
    # print(absent_days)

    comp_off = Attendance.objects.filter(is_active=1, is_present=2, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(comp_off)

    zipped_data = zip(dates, date_no)
    # print(date_no)
    employees = Employee.objects.filter(is_active=1)

    holidays = Holiday_Detail.objects.filter(
        is_active=1, date__range=[first_day, last_day])

    weekend = Weekend.objects.filter(is_active=1)
    # print(weekend)

    check_leave = Attendance.objects.filter(is_active = 1, date = myDate, is_leave = 1, is_leave_approved = 1, employee_id = request.user.emp_id)
    # print(check_leave)

    try:
        today_attn = Attendance.objects.get(is_active = 1, date = myDate, employee_id = request.user.emp_id)
        # print(today_attn.checkout_time)
    except Attendance.DoesNotExist:
        today_attn = None

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
        'check_leave':check_leave,
        'comp_off':comp_off,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'today_attn':today_attn,

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

    myDate = datetime.today()
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

   
    full_present_days = Attendance.objects.filter(is_active=1, is_present=1, is_half=0, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    
    half_present_days = Attendance.objects.filter(is_active=1, is_present=1, is_half=1, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    
    present_days = full_present_days + (half_present_days * 0.5)

    # print(present_days)

    comp_off = Attendance.objects.filter(is_active=1, is_present=2, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    
    full_absent_days = Attendance.objects.filter(is_active=1, is_leave=1, is_leave_approved = 1, is_half = 0, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
    
    half_absent_days = Attendance.objects.filter(is_active=1, is_leave=1, is_leave_approved = 1, is_half = 1, employee_id=request.user.emp_id, date__range=[first_day, last_day]).count()
   
    absent_days = full_absent_days + (half_absent_days * 0.5)
    # print(absent_days)

    holidays = Holiday_Detail.objects.filter(is_active=1, date__range=[first_day, last_day])

    weekend = Weekend.objects.filter(is_active=1)
    # print(weekend)

    check_leave = Attendance.objects.filter(is_active = 1, date = myDate, is_leave = 1, is_leave_approved = 1, employee_id = request.user.emp_id)
    # print(check_leave)

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
        'check_leave':check_leave,
        'comp_off':comp_off,
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

    employee = Employee.objects.get(employee_id=request.user.emp_id)
    # print(employee.date_of_joining)
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
        'employee': employee,
    }

    return render(request, "self_service/leave_tracker.html",  context )


def apply_leave(request):
    form = Apply_Leave_Form()
    employee = Employee.objects.get(is_active = 1, employee_id = request.user.emp_id)
    
    leaves = Leave_Applicable.objects.filter(is_active = 1, leave_type__is_active = 1, all_employees = 1).exclude(exception_dept = employee.department_id, exception_role = employee.role_id, exception_location = employee.location )
    
    leave_condition = Leave_Applicable.objects.filter(is_active = 1, leave_type__is_active = 1, all_employees = 0, gender = employee.gender, marital_status = employee.marital_status, department = employee.department_id, role = employee.role_id, location = employee.location, employment_type = employee.employee_type )
   
    if request.method == 'POST':
       
        form = Apply_Leave_Form(request.POST)
        #return HttpResponse('ve')
        if form.is_valid():
           #return HttpResponse('ve')   
           leave = request.POST.get('leave_type')
           #return HttpResponse(leave)
           for each in Leave_Type.objects.filter(is_active='1', id = leave):
                leave_type = each.type
                leave_name = each.name
                leave_unit = each.unit
                leave_id = each.id
                for each_restrict in Leave_Restrictions.objects.filter(is_active='1', leave_type_id=leave):
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

                    emp_id = request.POST.get('employee_id')
                    
                    from_date = datetime.strptime(request.POST.get('from_date'), '%d-%m-%Y')
                    to_date = datetime.strptime(request.POST.get('to_date'), '%d-%m-%Y')
                    reason = request.POST.get('reason')
                    created_at = timezone.now()
                    updated_at = timezone.now()

                    start_date = datetime.strptime(request.POST.get('from_date'), "%d-%m-%Y")
                    end_date = datetime.strptime(request.POST.get('to_date'), "%d-%m-%Y")
                    diff = abs((end_date-start_date).days)+1
                    #total_days = diff

                    delta = end_date - start_date
                    total_days = delta.days + 1


                    # return HttpResponse(total_days)
                   
                    message = "";
                    if (leave_name.strip() == "Sick Leave") and (total_days > 3):
                        message = "More than three days documents should be upload for sick leave";
                    if (str(total_days) < str(minimum_leave_apply))   and (minimum_leave_apply != None):
                         # if total_days != 0:
                           message = "Minimum " + minimum_leave_apply  + " leave that can be availed per application";
                          #return HttpResponse(message)
                    if (message == "") and (maximum_leave_apply != None):
                         if(int(total_days) >  int(maximum_leave_apply)):
                          message = "Maximum " + maximum_leave_apply  + " leave that can be availed per application";
                    if (message == "") and (maximum_consecutive_leave_apply != None):
                         if(int(total_days) > int(maximum_consecutive_leave_apply)):
                          message = "Maximum " + maximum_consecutive_leave_apply  + "  number of consecutive days of Leave allowed";
                    if  minimum_gap_apply != None:
                        applic = "ok"
                           # return HttpResponse(minimum_gap_apply)
                        
                        last_applied =  LeaveRequest.objects.filter(employee_id=emp_id).order_by('from_date').reverse()
                        # return HttpResponse(last_applied[0].from_date)
                        last_leave_d = 0
                        if last_applied != None and  len(last_applied) > 0:
                            last_applied_leave_date = last_applied[0].to_date
                            
                            date_format = "%Y-%m-%d"
                            last_leave_d = (str(last_applied_leave_date))
                            #return HttpResponse(datetime_object)
                        
                            datetime_object = datetime.strptime(last_leave_d, '%Y-%m-%d').date()
                            from_date1 = from_date.strftime('%Y-%m-%d')
                            datetime_object1 = datetime.strptime(from_date1, '%Y-%m-%d').date()
                            #return HttpResponse(datetime_object1)
                            delta = datetime_object1 - datetime_object
                            total_days1 = delta.days
                            #return HttpResponse(total_days) 
                        
                            if(int(minimum_gap_apply) >= int(total_days1)):
                                    applic = "ok" 
                                    message = "Require minimum " + minimum_gap_apply + " days gap  between two applications ! "
                                #return HttpResponse(message)
                    if message == "":
                    
                        delta = end_date - start_date       # as timedelta

                        Photo_name = ""
                        
                        if request.FILES:
                            
                            upload = request.FILES['document_url']
                            #
                            if upload != None: 
                                logoRoot = os.path.join(settings.MEDIA_ROOT, 'leave_documents/')
                            
                                #logo_url = os.path.join(settings.MEDIA_URL, 'profile_images/')
                                logoRoot=logoRoot.replace("\\","/")
                                Photo_name = upload.name
                                realVar = Photo_name.replace(" ", '')
                                Photo_name = realVar
                            # return HttpResponse(upload.name) 
                                fs = FileSystemStorage(location=logoRoot)
                                file_name = fs.save(Photo_name, upload)
                                file_url = fs.url(file_name)   
                                #return HttpResponse(file_url) 
                        #return HttpResponse(Photo_name)

                        if  LeaveRequest.objects.filter( Q(employee_id=Employee.objects.get(employee_id = emp_id)),Q(is_active='1'),Q(from_date__lte=start_date, to_date__gte=start_date) | Q(from_date__lte=end_date, to_date__gte=end_date)| Q(from_date__gte=start_date, to_date__gte=start_date) | Q(from_date__gte=end_date, to_date__gte=end_date)).exists():
                            # print('hdbn')
                            messages.error(request,'For this Date Leave had been  requested Already! ')
                            context = {'form': form}
                            return render(request, "self_service/apply_leave.html", context)

                        obj = LeaveRequest.objects.create( 
                            employee=Employee.objects.get(employee_id = emp_id) if emp_id else None, 
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
                            document_url=Photo_name

                        ) 
                        obj.save()

                        for i in range(delta.days + 1):
                         day = start_date + timedelta(days=i)
                        # print(datetime.strftime(day, "%d-%m-%Y"))  
                        insert = Attendance.objects.create(date=datetime.strftime(day, "%Y-%m-%d"), employee_id= emp_id, is_leave = 1 )

                        messages.success(request, 'Leave Requested Successfully ! ')
                        return redirect('leave_tracker') 

                    context = {
                    'form' : form,
                    'leaves' : leaves,
                    'leave_condition':leave_condition,
                    }
                    messages.error(request, message)
                    return render(request, "self_service/apply_leave.html",  context )

                    # context.update({"form": form})
                    # return render(request, "employee/add_employee.html", context)
                    # html_template = loader.get_template('self_service/apply_leave.html')
                  #  return HttpResponse(message) 
    
    # print(leaves)

    context = {
        'form' : form,
        'leaves' : leaves,
        'leave_condition':leave_condition,
    }

    return render(request, "self_service/apply_leave.html",  context )


def leave(request,leave):
    path = request.path.split("/")
    # print(path[2])
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

            if  LeaveRequest.objects.filter( Q(employee_id=Employee.objects.get(employee_id = emp_id)),Q(is_active='1'),Q(from_date__lte=start_date, to_date__gte=start_date) | Q(from_date__lte=end_date, to_date__gte=end_date)| Q(from_date__gte=start_date, to_date__gte=start_date) | Q(from_date__gte=end_date, to_date__gte=end_date)).exists():
                # print('hdbn')
                messages.error(request,'For this Date Leave had been requested Already! ')
                context = {'form': form}
                return render(request, "self_service/apply_leave.html", context)

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

def self_travel_request(request):
    requests = Travel_Request_Detail.objects.filter(is_active='1', employee_id = request.user.emp_id).order_by('-created_at')
    context = {'requests':requests}
    return render(request, "self_service/self_travel_request.html", context)


def add_self_travel_request(request):

    form = TarvelRequest_DetailForm()

    if request.method == 'POST':
        form = TarvelRequest_DetailForm(request.POST)
        if form.is_valid(): 
            employee = request.POST.get('employee')
            place_of_visit = request.POST.get('place_of_visit')
            employee_department = Employee.objects.filter(employee_id = employee, department__is_active = 1, is_active = 1)
            # print(employee_department)

            
            expected_date_of_arrival = request.POST.get('expected_date_of_arrival')
            if expected_date_of_arrival != "":
               #return HttpResponse(date)   
               d = datetime.strptime(expected_date_of_arrival, '%d-%m-%Y')
               expected_date_of_arrival = d.strftime('%Y-%m-%d')
            else:
               expected_date_of_arrival = None  

            expected_date_of_depature = request.POST.get('expected_date_of_depature')
            if expected_date_of_depature != "":
               #return HttpResponse(date)   
               d = datetime.strptime(expected_date_of_depature, '%d-%m-%Y')
               expected_date_of_depature = d.strftime('%Y-%m-%d')
            else:
               expected_date_of_depature = None   

            expected_duration_days = request.POST.get('expected_duration_days')

            purpose_of_visit = request.POST.get('purpose_of_visit')

            billable_to_customer = None


            customer_name = request.POST.get('customer_name')    
            
            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'

            obj = Travel_Request_Detail.objects.create( 

            employee_id=employee, 
            place_of_visit=place_of_visit,
            expected_date_of_arrival=expected_date_of_arrival,
            expected_date_of_depature=expected_date_of_depature,
            expected_duration_days=expected_duration_days,
            purpose_of_visit=purpose_of_visit,
            customer_name=customer_name,
            employee_department=employee_department[0].department.name,
            billable_to_customer=billable_to_customer,
            created_at=created_at, updated_at=updated_at, is_active=is_active,

            ) 
               # return HttpResponse(employee)   
            obj.save()
            messages.success(request, 'travel request details was added ! ')
            return redirect('/')

    context = {
          'form': form,
    }
   
    return render(request, "self_service/add_self_travel_request.html", context )



def delete_travel_request(request, pk):
   # return HttpResponse('working..')
    data = Travel_Request_Detail.objects.get(id =pk)
    data.is_active = 0
    data.save()
    messages.error(request, 'Travel request was deleted! ')
    return redirect('self_travel_request')

def self_travel_expense(request):
   # return HttpResponse("employee")
    employee = Travel_Expense_Detail.objects.filter(is_active='1',employee_id=request.user.emp_id)
    # print(employee)
    context = {'employees':employee}
    return render(request, "self_service/self_travel_expense.html", context)

def compensatory_request(request):
    data = Compoensatory_Request_Detail.objects.filter(is_active='1', employee_id = request.user.emp_id).order_by('-created_at')
    # print(employee)
    context = {'employees':data}
    return render(request, "self_service/compensatory_request.html", context)

def add_compensatory_request(request):
    form = CompensatoryRequest_DetailForm()
    if request.method == 'POST':
        form = CompensatoryRequest_DetailForm(request.POST)
        if  form.is_valid(): 
            # return HttpResponse('working.') 
            employee = request.POST.get('employee')
            unit = request.POST.get('unit')
            duration = request.POST.get('duration')
            
            compoensatory_date = request.POST.get('compoensatory_date')
            if compoensatory_date != "":
               d = datetime.strptime(compoensatory_date, '%d-%m-%Y')
               compoensatory_date = d.strftime('%Y-%m-%d')
            else:
               compoensatory_date = None  

            worked_date = request.POST.get('worked_date')
            if worked_date != "":
               d = datetime.strptime(worked_date, '%d-%m-%Y')
               worked_date = d.strftime('%Y-%m-%d')
            else:
               worked_date = None  

            ftime = request.POST.get('clockpicker_one')
            from_time = datetime.strptime(ftime, '%H:%M:%S')
            ttime = request.POST.get('clockpicker_two')
            to_time = datetime.strptime(ttime, '%H:%M:%S')
            reason = request.POST.get('reason')

            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')

            obj = Compoensatory_Request_Detail.objects.create( 

                employee_id=employee, 
                worked_date=worked_date,
                compoensatory_date=compoensatory_date,
                unit=unit,
                duration=duration,
                from_time=from_time,
                to_time=to_time,
                reason=reason,
                created_at=created_at, 
                updated_at=updated_at, 
                is_active=1,

            ) 
            obj.save()
            messages.success(request, 'Compensatory request was requested ! ')
            return redirect('compensatory_request') 

    context = {
          'form': form,
    }

    return render(request, "self_service/add_compensatory_request.html", context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'self_service/change_password.html', {
        'form': form
    })