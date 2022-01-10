from app.models import timelogs
from app.views.restriction_view import admin_only,role_name
from app.views.employee_view import employees
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.EmployeeForm import EmployeeForm 
from app.forms.LeaveTypeForm import LeaveTypeForm

#from app.forms import UserGroupForm  

from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
from app.models.leave_type_model import * 
from app.models.leave_balance_model import *
from app.models.department_model import *
from app.models.role_model import *
# from app.models.leave_balance_model import *
# from app.models import Group 

#from app.models import Group 
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q, query
from datetime import datetime
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
import MySQLdb
from itertools import chain
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.db import connection,transaction
from django.db.models import F
from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
import datetime
from app.models.attendance_model import Attendance
from app.models.announcement_model import Announcement 
from app.models.weekend_model import Weekend
from django.core.exceptions import PermissionDenied
from app.models.holiday_details_model import Holiday_Detail 
from app.models.leave_balance_model import Leave_Balance
from app.models.project_model import Project
from app.models.timelogs import TimeLogs
from django.conf import settings

from django_seed import Seed

import logging
logger = logging.getLogger(__name__)

#from app.models import QuillModel

@login_required
def index(request):

    # print(request.session['checkin_session'])

    dept_count = Department.objects.all().count()
    role_count = Group.objects.all().count()
    emp_count = Employee.objects.all().count()
    # print(emp_count)

    if dept_count == 0 and role_count == 0 and emp_count == 0:
       
        seeder = Seed.seeder()
        # seeder.add_entity(Department, 1)
        # seeder.add_entity(Group, 1)
        seeder.add_entity(Department, 1, {
            'name': 'Admin',
            'description': 'This is admin dept..',
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'added_by': None,
            'updated_by': None,
            'is_active': 1,
            'device':'web',
        })
        seeder.add_entity(Group, 1, {
            'name': 'Admin',
            'description': 'This is admin role..',
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'created_by': None,
            'is_active': 1,
            'role_type': 'admin',
        })
        seeder.add_entity(Employee, 1, {
            'employee_id': 'Emp001',
            'first_name': 'Admin',
            'last_name': 'Admin',
            'nick_name':'admin',
            'email_id': 'admin@gmail.com',
            'mobile_number': '9874563210',
            'department_id': 1,
            'source_of_hire':None,
            'seating_location':None,
            'location_id':None,
            'title':None,
            'date_of_joining':None,
            'employee_status':'Active',
            'employee_type':'Permenant',
            'work_phone':None,
            'extension':None,
            'total_experience':None,
            'experience':None,
            'mobile_phone':None,
            'other_email':None,
            'birth_date':None,
            'marital_status':None,
            'address':None,
            'tags':None,
            'job_description':None,
            'expertise':None,
            'date_of_exit':None,
            'gender':None,
            'about_me':None,
            'code_name':None,
            'code_num':None,
            'emirate_id':None,
            'profile':None,
            'signature':None,
            'passport_exp_date':None,
            'passport_num':None,
            'psssport_url':None,
            'role_id': 1,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'is_active': 1,
        })

        seeder.execute()

        update_usr = User.objects.filter(id=request.user.id).update( 
            emp_id='Emp001',
            role = 1,
        )

        return redirect('/home/')

    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')

    # del request.session['checkin_session']
    myDate = datetime.date.today()
   
    query = Employee.objects.filter(role__is_active ='1', department__is_active ='1', birth_date= datetime.date.today() )

    role = role_name(request)
    # print(role)

    # last 15 days records
    new_hires = Employee.objects.filter(is_active = 1, created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=15))

    # last 3 records
    # new_hires = Employee.objects.filter(is_active = 1).order_by('-created_at')[:3]
    # print(new_hires)

    tdelta = 0
    myDate = datetime.date.today()
    check_in_time = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id, is_present = 1)
    # print(check_in_time[0].checkin_time) 
    # t1 = request.session['checkin_session']
    if check_in_time:
        if check_in_time[0].checkin_time:
            t1 = check_in_time[0].checkin_time.strftime('%H:%M:%S')

        if check_in_time[0].checkout_time:
            if 'checkin_session' in request.session:
                t2 = datetime.datetime.now().strftime('%H:%M:%S')
            else:
                t2 = check_in_time[0].checkout_time.strftime('%H:%M:%S')
        else:   
            t2 = datetime.datetime.now().strftime('%H:%M:%S')
        FMT = '%H:%M:%S'
        tdelta = datetime.datetime.strptime(t2, FMT) - datetime.datetime.strptime(t1, FMT)
        # print(tdelta)
        # check_in = tdelta.seconds/3600
        # print(check_in)

    announcements = Announcement.objects.filter(added_by__is_active = 1, created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30), expiry_date__gte=datetime.datetime.today() ).order_by('-created_at')
    # print(announcements)

    start_week = myDate - datetime.timedelta(myDate.weekday())
    end_week = start_week + datetime.timedelta(7)
   
    week_atten = Attendance.objects.filter(is_active = 1,  employee_id = request.user.emp_id, date__range=[start_week, end_week])

    holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[start_week, end_week]) 
    # print(holidays)

    leaves = Leave_Balance.objects.filter(is_active = 1, leave_type__is_active = 1, employee_id=request.user.emp_id) 
    # print(leaves[0].leave_type.name)

    weekend = Weekend.objects.filter(is_active = 1)
    # print(weekend)

    # upcoming_holidays = Holiday_Detail.objects.filter(is_active = 1, date__gt= datetime.datetime.now())[:5]
    # print(upcoming_holidays)

    location_employee=Employee.objects.filter(is_active='1',employee_id=request.user.emp_id).get()
    location_id=location_employee.location

    upcoming_holidays = Holiday_Detail.objects.filter(is_active = 1,applicable_location=location_id, date__gt= datetime.datetime.now())[:5]
    # print(upcoming_holidays)

    leave_today = Attendance.objects.filter(is_active = 1, date = myDate, is_leave = 1, is_leave_approved = 1, employee__is_active = 1, employee__department__is_active = 1)
    # print(leave_today[0].employee.mobile_number)

    check_leave = Attendance.objects.filter(is_active = 1, date = myDate, is_leave = 1, is_leave_approved = 1, is_half = 0, employee_id = request.user.emp_id)
    # print(check_leave)

    timelogs = TimeLogs.objects.filter(is_active = 1, date__range=[start_week, end_week], employee_id = request.user.emp_id, project__is_active = 1)
    # print(timelogs)
    
   
    try:
        today_attn = Attendance.objects.get(is_active = 1, date = myDate, employee_id = request.user.emp_id)
        # print(today_attn.checkout_time)
    except Attendance.DoesNotExist:
        today_attn = None

    # print(today_attn)

    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    now = datetime.datetime.now()

    now_day_1 = now - datetime.timedelta(days=now.weekday())

    dates = []
    date_no = []

    for n_week in range(1):
        dates= [(now_day_1 + datetime.timedelta(days=d+n_week*7)) for d in range(7)]
        date_no= [(now_day_1 + datetime.timedelta(days=d+n_week*7)).strftime("%d") for d in range(7)]

        # dates.append( (now_day_1 + datetime.timedelta(days=d+n_week*7)).strftime("%Y-%m-%d") for d in range(7) )
        # date_no.append( (now_day_1 + datetime.timedelta(days=d+n_week*7)).strftime("%d") for d in range(7) )

    zipped_data = zip(weekdays, date_no, dates)
    days_and_no = zip(date_no, weekdays, dates )
    # print(weekdays)
    if check_in_time:
        if check_in_time[0].checkin_time:
            login_time = str(check_in_time[0].checkin_time)
        else:
            login_time = ""
    else:
        login_time = ""

    #return HttpResponse(settings.GOOGLE_MAPS_API_KEY)
    if 'checkin_session' in request.session:
        session = request.session['checkin_session']
    else:
        session = ""

    # print(session)

    current_emp = Employee.objects.filter(is_active = 1, employee_id= request.user.emp_id)
    
    current_emp_passport_date =  current_emp[0].passport_exp_date
    #return HttpResponse(current_emp_passport_date) 
    expire = 0
    if current_emp_passport_date != None:  
          to_date = datetime.datetime.now().strftime('%Y-%m-%d')
          delta = current_emp_passport_date - date.today()
             
          expire = 0
          if delta.days < 0:
                  expire = 1
          #return HttpResponse(expire) 

  
    context = {
        'birthdays':query,
        'check_in':tdelta,
        'new_hires':new_hires,
        'announcements':announcements,
        'week_atten':week_atten,
        'weekdays':zipped_data,
        'days_and_no':days_and_no,
        'holidays':holidays,
        'upcoming_holidays':upcoming_holidays,
        'weekend':weekend,
        'leaves':leaves,
        'leave_today':leave_today,
        'login_time':login_time,
        'session': session,
        'check_leave':check_leave,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'expiry': expire,
        'timelogs':timelogs,
        'today_attn':today_attn,

    }

    return render(request, "dashboard/dashboard.html", context)

    
