from django import http
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from app.views.restriction_view import admin_only,role_name
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.utils import timezone
from app.models import weekend_model
from app.models.employee_model import Employee
from app.models.holiday_details_model import Holiday_Detail 
from app.models.reporting_to_model import Reporting
from app.models.weekend_model import Weekend
import datetime 
from datetime import date, time, datetime, timedelta
from django.db.models import Q
import calendar
from app.models.attendance_model import Attendance 
from django.contrib.auth.models import Group
from io import BytesIO
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
import json
import xlsxwriter
#from geopy.geocoders import Nominatim
#from django.contrib.gis.utils import GeoIP
import socket
#

@login_required(login_url="/login/")
def check_in_attn(request):
    if request.method == 'POST':
        
        # return HttpResponse(request.POST.get('checkin_lat')) 

        myDate = datetime.now()
        if not Attendance.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, is_active = 1)).exists():
           
            insert = Attendance.objects.create(
                date=myDate, 
                checkin_time=datetime.now().strftime('%H:%M:%S'), 
                checkin_location = request.POST.get('checkin_location'),
                checkin_lat = request.POST.get('checkin_lat'),
                checkin_lang = request.POST.get('checkin_lang'),
                employee_id= request.user.emp_id,
                checkin_active=1, 
                checkout_active=0, 
            )

            request.session['checkin_session'] = datetime.now().strftime('%H:%M:%S')
            if not Attendance.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, is_leave=1, is_active = 1)).exists():
                update = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id ).update(
                    is_present = 1,
                )
            messages.success(request,' Checked in successfully ')
            # return redirect('home')
            return redirect(request.META.get('HTTP_REFERER'))

            
        else:

            if Attendance.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, is_wfh_approved = 1, is_active = 1, checkin_time__isnull=True)).exists():    
                update = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id ).update(
                    checkin_time=datetime.now().strftime('%H:%M:%S'), 
                    checkin_location = request.POST.get('checkin_location'),
                    checkin_lat = request.POST.get('checkin_lat'),
                    checkin_lang = request.POST.get('checkin_lang'),
                    created_at = datetime.now(),
                    updated_at = datetime.now(),
                    is_present = 1,
                    checkin_active=1, 
                    checkout_active=0, 
                )
                request.session['checkin_session'] = datetime.now().strftime('%H:%M:%S')
            else:
                update = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id, is_active = 1 ).update(
                    checkin_location = request.POST.get('checkin_location'),
                    checkin_lat = request.POST.get('checkin_lat'),
                    checkin_lang = request.POST.get('checkin_lang'),
                    updated_at = datetime.now(),
                    checkin_active=1, 
                    checkout_active=0, 
                )
                request.session['checkin_session'] = datetime.now().strftime('%H:%M:%S')
            # print(request.session['checkin_session'])

   
    return redirect(request.META.get('HTTP_REFERER'))

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP 

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip    

def check_out_attn(request):
    if request.method == 'POST':
        myDate = datetime.now()
        if Attendance.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, is_active = 1)).exists():
            update = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id ).update(
                checkout_time = datetime.now().strftime('%H:%M:%S'),
                checkout_location = request.POST.get('checkout_location'),
                checkout_lat = request.POST.get('checkout_lat'),
                checkout_lang = request.POST.get('checkout_lang'),
                updated_at = datetime.now(),
                checkout_active=1, 
                
            )
            if 'checkin_session' in request.session:
                del request.session['checkin_session']
            messages.success(request,' Checked out successfully ')
            # return redirect('home')
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            if 'checkin_session' in request.session:
                del request.session['checkin_session']
            messages.success(request,' Checked out successfully ')
            # return redirect('home')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


def attn_listview(request):

    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    month_year = current_month+'-'+current_year
    first_day = now.replace(day = 1)
    last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])
    # no_of_days = calendar.monthrange(current_year, current_month )

    role = role_name(request)
    # print(role)

    
    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append( (first_day + timedelta(days=i)) )
        date_no.append( (first_day + timedelta(days=i)).strftime("%d") )

    # print(dates)

    month_atten = Attendance.objects.filter(is_active = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day])
    # print(month_atten)

    present_days = Attendance.objects.filter(is_active = 1, is_present = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(present_days)

    half_present = Attendance.objects.filter(is_active = 1, is_half = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    
    present_days = present_days + (half_present * 0.5)

    # print(present_days)

    absent_days = Attendance.objects.filter(is_active = 1, is_leave = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(absent_days)

    comp_off = Attendance.objects.filter(is_active = 1, is_present = 2, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(comp_off)

    zipped_data = zip(dates, date_no)
    # print(date_no)

    if role =="Admin":
        employees = Employee.objects.filter(is_active = 1)
    if role =="Manager":
        employees = Reporting.objects.select_related().filter(Q(is_active=1) & Q(reporting_id=request.user.emp_id) )
        # print(reporting)

    holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 

    weekend = Weekend.objects.filter(is_active = 1)
    # print(weekend)

    num_days = len([1 for i in calendar.monthcalendar(datetime.now().year,datetime.now().month) if i[6] != 0])

 
    context = {
        'month_atten':month_atten,
        'holidays':holidays,
        'zipped_data':zipped_data,
        'employees':employees,
        'present_days':present_days,
        'absent_days':absent_days,
        'month':now.strftime("%b"),
        'month_no':now.strftime("%m"),
        'year':now.strftime("%Y"),
        'emp_id':request.user.emp_id,
        'weekend':weekend,
        'weekend_count':num_days,
        'comp_off':comp_off,

    }

    return render(request, "attendance/attn_list.html",context)



def search_listview(request,pk,month):
   
    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    # first_day = now.replace(day = 1)
    # last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])
    # no_of_days = calendar.monthrange(current_year, current_month )
    date = datetime.strptime(month, "%m-%Y")
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    # print(date.strftime("%Y"))

    role = role_name(request)
    # print(role)

    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append( (first_day + timedelta(days=i)) )
        date_no.append( (first_day + timedelta(days=i)).strftime("%d") )

    month_atten = Attendance.objects.filter(is_active = 1,  employee_id = pk, date__range=[first_day, last_day])
    # print(month_atten)

    zipped_data = zip(dates, date_no)
#    print(zipped_data)
    
    if role =="Admin":
        employees = Employee.objects.filter(is_active = 1)
    if role =="Manager":
        employees = Reporting.objects.select_related().filter(Q(is_active=1) & Q(reporting_id=request.user.emp_id) )
        # print(reporting)

    present_days = Attendance.objects.filter(is_active = 1, is_present = 1, employee_id = pk, date__range=[first_day, last_day]).count()
    # print(present_days)

    half_present = Attendance.objects.filter(is_active = 1, is_half = 1, employee_id = pk, date__range=[first_day, last_day]).count()
    
    present_days = present_days + (half_present * 0.5)

    # print(present_days)

    absent_days = Attendance.objects.filter(is_active = 1, is_leave = 1, is_half = 0, employee_id=pk, date__range=[first_day, last_day]).count()
    # print(absent_days)

    half_days = Attendance.objects.filter(is_active = 1, is_leave = 1, is_half = 1, employee_id = pk, date__range=[first_day, last_day]).count()
    # print(half_days * 0.5)

    absent_days = absent_days + (half_days * 0.5)
    # print(absent_days)


    comp_off = Attendance.objects.filter(is_active = 1, is_present = 2, employee_id = pk, date__range=[first_day, last_day]).count()
    # print(comp_off)

    holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 
 
    weekend = Weekend.objects.filter(is_active = 1)
    # print(weekend)

    num_days = len([1 for i in calendar.monthcalendar(datetime.now().year,datetime.now().month) if i[6] != 0])

 
    context = {
        'month_atten':month_atten,
        'holidays':holidays,
        'zipped_data':zipped_data,
        'employees':employees,
        'present_days':present_days,
        'absent_days':absent_days,
        'search_id':pk,
        'month':date.strftime("%b"),
        'month_no':date.strftime("%m"),
        'year':date.strftime("%Y"),
        'emp_id':pk,
        'weekend':weekend,
        'weekend_count':num_days,
        'comp_off':comp_off,
    }
    

    return render(request, "attendance/attn_list.html",context)


def attn_tableview(request):
    
    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    month_year = current_month+'-'+current_year
    first_day = now.replace(day = 1)
    last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])
    # no_of_days = calendar.monthrange(current_year, current_month )
    
    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append( (first_day + timedelta(days=i)) )
        date_no.append( (first_day + timedelta(days=i)).strftime("%d") )

    month_atten = Attendance.objects.filter(is_active = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day])
    # print(month_atten)

    present_days = Attendance.objects.filter(is_active = 1, is_present = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
   
    half_present = Attendance.objects.filter(is_active = 1, is_half = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    
    present_days = present_days + (half_present * 0.5)
    # print(present_days)

    absent_days = Attendance.objects.filter(is_active = 1, is_leave = 1, is_half = 0, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(absent_days)

    half_days = Attendance.objects.filter(is_active = 1, is_leave = 1, is_half = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(half_days * 0.5)

    absent_days = absent_days + (half_days * 0.5)
    # print(absent_days)

    comp_off = Attendance.objects.filter(is_active = 1, is_present = 2, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(comp_off)

    zipped_data = zip(dates, date_no)
#    print(zipped_data)
    employees = Employee.objects.filter(is_active = 1)

    holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 
    
    weekend = Weekend.objects.filter(is_active = 1)
    # print(weekend)

    year = 2021
    month = 10
    day_to_count = calendar.SUNDAY
   
    
    num_days = len([1 for i in calendar.monthcalendar(datetime.now().year,datetime.now().month) if i[6] != 0])

    # print(num_days)
 
    context = {
        'month_atten':month_atten,
        'holidays':holidays,
        'zipped_data':zipped_data,
        'employees':employees,
        'present_days':present_days,
        'absent_days':absent_days,
        'month':now.strftime("%b"),
        'month_no':now.strftime("%m"),
        'year':now.strftime("%Y"),
        'emp_id':request.user.emp_id,
        'weekend':weekend,
        'weekend_count':num_days,
        'comp_off':comp_off,

    }

    return render(request, "attendance/attn_tabular.html",context)

def weeknum(dayname):
    if dayname == 'Monday':   return 0
    if dayname == 'Tuesday':  return 1
    if dayname == 'Wednesday':return 2
    if dayname == 'Thursday': return 3
    if dayname == 'Friday':   return 4
    if dayname == 'Saturday': return 5
    if dayname == 'Sunday':   return 6

def search_tableview(request,pk,month):
   
    now = datetime.now()
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    # first_day = now.replace(day = 1)
    # last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])
    # no_of_days = calendar.monthrange(current_year, current_month )
    date = datetime.strptime(month, "%m-%Y")
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    # print(date.strftime("%Y"))

    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append( (first_day + timedelta(days=i)) )
        date_no.append( (first_day + timedelta(days=i)).strftime("%d") )

    month_atten = Attendance.objects.filter(is_active = 1,  employee_id = pk, date__range=[first_day, last_day])
    # print(month_atten)

    zipped_data = zip(dates, date_no)
#    print(zipped_data)
    employees = Employee.objects.filter(is_active = 1)


    present_days = Attendance.objects.filter(is_active = 1, is_present = 1, employee_id = pk, date__range=[first_day, last_day]).count()
   
    half_present = Attendance.objects.filter(is_active = 1, is_half = 1, employee_id = pk, date__range=[first_day, last_day]).count()
    
    present_days = present_days + (half_present * 0.5)
    # print(present_days)

    absent_days = Attendance.objects.filter(is_active = 1, is_leave = 1, is_half = 0, employee_id = pk, date__range=[first_day, last_day]).count()
    # print(absent_days)

    half_days = Attendance.objects.filter(is_active = 1, is_leave = 1, is_half = 1, employee_id = pk, date__range=[first_day, last_day]).count()
    # print(half_days * 0.5)

    absent_days = absent_days + (half_days * 0.5)
    # print(absent_days)

    comp_off = Attendance.objects.filter(is_active = 1, is_present = 2, employee_id = pk, date__range=[first_day, last_day]).count()
    # print(comp_off)

    holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 
 
    weekend = Weekend.objects.filter(is_active = 1)
    # print(weekend)

    num_days = len([1 for i in calendar.monthcalendar(datetime.now().year,datetime.now().month) if i[6] != 0])

    context = {
        'month_atten':month_atten,
        'holidays':holidays,
        'zipped_data':zipped_data,
        'employees':employees,
        'present_days':present_days,
        'absent_days':absent_days,
        'search_id':pk,
        'month':date.strftime("%b"),
        'month_no':date.strftime("%m"),
        'year':date.strftime("%Y"),
        'emp_id':pk,
        'weekend':weekend,
        'weekend_count':num_days,
        'comp_off':comp_off,
    }
    

    return render(request, "attendance/attn_tabular.html",context)

def export_excel(request):
        
    # create a workbook in memory
    output = BytesIO()

    date = datetime.strptime(request.POST.get('month'), "%m-%Y")
    # print(date.strftime("%B"))
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])

    dates = []
    date_no = []

    delta = last_day - first_day

    for i in range(delta.days + 1):
        dates.append( (first_day + timedelta(days=i)) )
        date_no.append( (first_day + timedelta(days=i)).strftime("%d") )

    # print(date_no)

    book = xlsxwriter.Workbook(output)
        
    # Set up some formats to use.
    bold = book.add_format({'bold': True})
    weekend_color = book.add_format({'font_color': '#ff8700'})
    absent_color = book.add_format({'font_color': '#f0989a'})
    holiday_color = book.add_format({'font_color': '#0de2ff'})
    present_color = book.add_format({'font_color': '#3dce4c'})
    comp_off_color = book.add_format({'font_color': '#3d81ce'})

    format1 = book.add_format({'border': 1})

    format2 = book.add_format({'border': 1, 'bold': True })

    # print(request.POST.get('type'))

    role = role_name(request)
    # print(role)

    if role =="Admin":
        if request.POST.get('type') == "All":
            employees = Employee.objects.filter(is_active = 1)
        
        if request.POST.get('type') == "Selected":
            employees = Employee.objects.filter(is_active = 1, employee_id = request.POST.get('employee_id'))

    
    if role =="Manager":
        if request.POST.get('type') == "All":

            emp_ids = []
            emp_ids.append(request.user.emp_id)
            reporing = Reporting.objects.select_related().filter(Q(is_active=1) & Q(reporting_id=request.user.emp_id) )

            for report in reporing:
                emp_ids.append(report.employee.employee_id)

            # print(emp_ids)    

            employees = Employee.objects.filter(is_active = 1, employee_id__in = emp_ids)
          
        if request.POST.get('type') == "Selected":
            employees = Employee.objects.filter(is_active = 1, employee_id = request.POST.get('employee_id'))

   
    holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 

    weekend = Weekend.objects.filter(is_active = 1)
    
    # print(employees)

    row_num = 2

    for emp in employees:
        # print(emp.employee_id)

        sheet = book.add_worksheet(emp.first_name +" "+emp.last_name)
        sheet.set_column(0, 3, 25)
        sheet.set_column(4, 4, 50)

        # format = sheet.add_format()
        # format.set_bottom(7)

        # sheet.conditional_format('B3:E4',
        #                      {'type': 'cell',
        #                       'criteria': '!=',
        #                       'value': 'None',
        #                       'format': format})

        sheet.write('B3', 'Employee Name', bold)
        sheet.write('B4', 'Employee ID', bold)
        sheet.write('C3', emp.first_name +" "+emp.last_name)
        sheet.write('C4', emp.employee_id)

        sheet.conditional_format('B3:E4', { 'type' : 'no_blanks' , 'format' : format1})
        

        sheet.write('D3', 'Month / Year', bold)
        sheet.write('E3', date.strftime("%B")+ "/"+date.strftime("%Y"))

        sheet.write('A7', 'Date', bold)
        sheet.write('B7', 'Status', bold)
        sheet.write('C7', 'First Check-In', bold)
        sheet.write('D7', 'Last Check-Out', bold)
        sheet.write('E7', 'Check-In Location', bold)

        month_atten = Attendance.objects.filter(is_active = 1,  employee_id = emp.employee_id, employee__is_active = 1, date__range=[first_day, last_day])
        # print(month_atten)

        row_num = 8
        present_days = 0
        absent_days = 0

        for date in dates:

            sheet.write('A'+str(row_num), (date).strftime("%d-%m-%Y"))
            
            for row_data in month_atten.iterator():
                
                date_time_attn = datetime.strptime(str(row_data.date), '%Y-%m-%d')
                # print(date_time_attn)

                if date_time_attn == date:
                    
                    if row_data.is_present == 1:
                        sheet.write('B'+str(row_num), "Present", present_color)
                        present_days += 1
                    if row_data.is_present == 2:
                        sheet.write('B'+str(row_num), "Comp Off", comp_off_color)
                        present_days += 1
                    if row_data.is_leave == 1 and row_data.is_half == 0:
                        sheet.write('B'+str(row_num), "Absent", absent_color)
                        absent_days += 1
                    if row_data.is_leave == 1 and row_data.is_half == 1:
                        sheet.write('B'+str(row_num), "Absent-HalfDay / Present", absent_color)
                        absent_days += 0.5
                        present_days += 0.5
                        
                    sheet.write('C'+str(row_num), (row_data.checkin_time ).strftime("%I:%M%p") if row_data.checkin_time else "-" )
                    sheet.write('D'+str(row_num), (row_data.checkout_time).strftime("%I:%M%p") if row_data.checkout_time else "-" )
                    sheet.write('E'+str(row_num), (row_data.checkin_location) if row_data.checkin_location else "-" )
                
            for holi in holidays:
                date_time_holi = datetime.strptime(str(holi.date), '%Y-%m-%d')
                
                if date_time_holi == date:
                    sheet.write('A'+str(row_num), (date).strftime("%d-%m-%Y"))
                    sheet.write('B'+str(row_num), holi.holiday_name	+ '(Holiday)', holiday_color)
                    sheet.write('C'+str(row_num), '-')
                    sheet.write('D'+str(row_num), '-')
                    sheet.write('E'+str(row_num), '-')

            for week in weekend:
                remove_single_quotes = week.week_off.replace("'", "")
                remove_square_brackets = str(remove_single_quotes)[1:-1]
                days_list = list(remove_square_brackets.split(","))
                
                day_no = []
                
                # print(date.strftime("%A"))

                for days in days_list:
                    day_name = days.capitalize()
                    if date.strftime("%A") == day_name:
                        sheet.write('A'+str(row_num), (date).strftime("%d-%m-%Y"))
                        sheet.write('B'+str(row_num), 'Weekend', weekend_color)
                        sheet.write('C'+str(row_num), '-')
                        sheet.write('D'+str(row_num), '-')
                        sheet.write('E'+str(row_num), '-')
            

            row_num += 1

        sheet.conditional_format('A7:E'+str(row_num), { 'type' : 'no_blanks' , 'format' : format1})

        row_num +=3
        
        for i in range(2):
            if i ==0:
                sheet.write('B'+str(row_num), 'Present Days', format2)
                sheet.write('C'+str(row_num), present_days, format2)
            if i ==1:
                sheet.write('B'+str(row_num), 'Absent Days', format2)
                sheet.write('C'+str(row_num), absent_days, format2)
           
            row_num += 1

        

    book.close()

    output.seek(0)

    # Set up the Http response.
    if request.POST.get('type') == "All":
        filename = "attendance-"+str(request.POST.get('month'))+'.xlsx'
    if request.POST.get('type') == "Selected":
        filename = emp.first_name+"_"+emp.last_name+"-"+str(request.POST.get('month'))+'.xlsx'

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

    # return HttpResponse('ok')


def attn_calendarview(request):

    employees = Employee.objects.filter(is_active = 1)

    context = {
        "employees":employees,
    }

    return render(request, "attendance/attn_calendar.html",context)


def show_cal_view(request):   
    #return HttpResponse('work')  

    from datetime import date, datetime, timedelta

    date = datetime.now()
    # print(now)
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    month_year = current_month+'-'+current_year
    
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    # print(first_day)
    month_atten = Attendance.objects.filter(is_active = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day])
    # print(month_atten)
    
    all_holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 

    weekend = Weekend.objects.filter(is_active = 1)
                                                                                       
    out = []                                                                                                             
    for attn in month_atten:     
        if attn.is_present == 1 and attn.is_wfh_approved == None:
            out.append({                                                                                                     
                'title': 'Present',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3dce4cd9',                                                           
            }) 
        elif attn.is_present == 1 and attn.is_wfh_approved == 1:
            out.append({                                                                                                     
                'title': 'Present / WFH',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3dce4cd9',                                                           
            })

        elif attn.is_half == 1:
            out.append({                                                                                                     
                'title': 'Absent - HalfDay / Present',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#f0989a',                                                           
            })

        elif attn.is_present == 2:
            out.append({                                                                                                     
                'title': 'Comp Off',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3d81ced9',                                                           
            }) 

        else:
            out.append({                                                                                                     
                'title': 'Absent',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'color': '#f0989a',                                                           
            })   

         
    for holi in all_holidays:                                                                                             
        out.append({                                                                                                     
            'title': holi.holiday_name,                                                                                         
            'id': holi.id,                                                                                              
            'start': holi.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
            'end': holi.date.strftime("%m/%d/%Y"),  
            'color': '#0de2ffd9',                                                           
        })        

            
    for week in weekend:
        # for day in week.week_off:
        remove_single_quotes = week.week_off.replace("'", "")
        remove_square_brackets = str(remove_single_quotes)[1:-1]
        days_list = list(remove_square_brackets.split(","))
        
        day_no = []

        for days in days_list:

            day_name = day_names(days.capitalize())
            
            weekend_dates = [first_day + timedelta(days=x) for x in range((last_day-first_day).days + 1) if (first_day + timedelta(days=x)).weekday() == day_name]
            # print(weekend_dates)  
            
            for w_day in weekend_dates:
                # print(w_day.strftime("%d"))
                if w_day.strftime("%d") not in day_no:
                    day_no.append(w_day.strftime("%d"))
                    out.append({                                                                                                     
                        'title': "Weekend",                                                                                         
                        'id': '0',                                                                                              
                        'start': w_day.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                        'end': w_day.strftime("%m/%d/%Y"),  
                        'color': '#ff8700',                                                           
                    })  
              

   
    return JsonResponse(out, safe=False)  

def day_names(name):
   
    if name =="Monday":
        return 0
    if name =="Tuesday":
        return 1
    if name =="Wednesday":
        return 2
    if name =="Thursday":
        return 3
    if name =="Friday":
        return 4
    if name =="Saturday":
        return 5
    if name =="Sunday":
        return 6



def show_attn_time(request):
    id = request.GET.get("id", None)
    data = Attendance.objects.filter(id=id)
    tmpJson = serializers.serialize("json",data)
    tmpObj = json.loads(tmpJson)
    
    return JsonResponse(tmpObj, safe=False)



def search_attn_time(request):   

    emp_id = request.GET.get("emp_id", None)

    # date = datetime.now()
    date = request.GET.get("date")
    # print(now)
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    month_year = current_month+'-'+current_year
    
    date_c = datetime.strptime(date, "%m/%d/%Y")
    first_day = date_c.replace(day = 1)
    last_day = date_c.replace(day = calendar.monthrange(date_c.year, date_c.month)[1])
    # print(first_day)
    
    month_atten = Attendance.objects.filter(is_active = 1, employee_id = emp_id, date__range=[first_day, last_day])
    # print(month_atten)
    
    all_holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 

    weekend = Weekend.objects.filter(is_active = 1)
                                                                            
    out = []                                                                                                             
    for attn in month_atten:     
        if attn.is_present == 1 and attn.is_wfh_approved == None:
            out.append({                                                                                                     
                'title': 'Present',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3dce4cd9',                                                           
            }) 
        elif attn.is_present == 1 and attn.is_wfh_approved == 1:
            out.append({                                                                                                     
                'title': 'Present / WFH',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3dce4cd9',                                                           
            })

        elif attn.is_half == 1:
            out.append({                                                                                                     
                'title': 'Absent - HalfDay / Present',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#f0989a',                                                           
            })
 
        elif attn.is_present == 2:
            out.append({                                                                                                     
                'title': 'Comp Off',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3d81ced9',                                                           
            })  
        else:
            out.append({                                                                                                     
                'title': 'Absent',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'color': '#f0989a',                                                           
            })   

         
    for holi in all_holidays:                                                                                             
        out.append({                                                                                                     
            'title': holi.holiday_name,                                                                                         
            'id': holi.id,                                                                                              
            'start': holi.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
            'end': holi.date.strftime("%m/%d/%Y"),  
            'color': '#0de2ffd9',                                                           
        })        

    for week in weekend:
        # for day in week.week_off:
        remove_single_quotes = week.week_off.replace("'", "")
        remove_square_brackets = str(remove_single_quotes)[1:-1]
        days_list = list(remove_square_brackets.split(","))
        
        day_no = []

        for days in days_list:

            day_name = day_names(days.capitalize())
            
            weekend_dates = [first_day + timedelta(days=x) for x in range((last_day-first_day).days + 1) if (first_day + timedelta(days=x)).weekday() == day_name]
            # print(weekend_dates)  
            
            for w_day in weekend_dates:
                # print(w_day.strftime("%d-%m-%Y"))
                if w_day.strftime("%d") not in day_no:
                    day_no.append(w_day.strftime("%d"))
                    out.append({                                                                                                     
                        'title': "Weekend",                                                                                         
                        'id': 1,                                                                                              
                        'start': w_day.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                        'end': w_day.strftime("%m/%d/%Y"),  
                        'color': '#ff8700',                                                           
                    })  
                

    return JsonResponse(out, safe=False)  


def search_attn_date(request):   

    date = request.GET.get("date")
    emp_id = request.GET.get("emp_id")
   
    date_c = datetime.strptime(date, "%m/%d/%Y")
    first_day = date_c.replace(day = 1)
    last_day = date_c.replace(day = calendar.monthrange(date_c.year, date_c.month)[1])
    # print(first_day)
    month_atten = Attendance.objects.filter(is_active = 1, employee_id = emp_id, date__range=[first_day, last_day])
    
    all_holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 

    weekend = Weekend.objects.filter(is_active = 1)
                                                                                       
    out = []                                                                                                             
    for attn in month_atten:     
        if attn.is_present == 1 and attn.is_wfh_approved == None:
            out.append({                                                                                                     
                'title': 'Present',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3dce4cd9',                                                           
            }) 
        elif attn.is_present == 1 and attn.is_wfh_approved == 1:
            out.append({                                                                                                     
                'title': 'Present / WFH',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3dce4cd9',                                                           
            })

        elif attn.is_half == 1:
            out.append({                                                                                                     
                'title': 'Absent - HalfDay / Present',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#f0989a',                                                           
            })
  
        elif attn.is_present == 2:
            out.append({                                                                                                     
                'title': 'Comp Off',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3d81ced9',                                                           
            })  
        else:
            out.append({                                                                                                     
                'title': 'Absent',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'color': '#f0989a',                                                           
            })   

         
    for holi in all_holidays:                                                                                             
        out.append({                                                                                                     
            'title': holi.holiday_name,                                                                                         
            'id': holi.id,                                                                                              
            'start': holi.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
            'end': holi.date.strftime("%m/%d/%Y"),  
            'color': '#0de2ffd9',                                                           
        })        

    for week in weekend:
        # for day in week.week_off:
        remove_single_quotes = week.week_off.replace("'", "")
        remove_square_brackets = str(remove_single_quotes)[1:-1]
        days_list = list(remove_square_brackets.split(","))
        
        day_no = []

        for days in days_list:

            day_name = day_names(days.capitalize())
            
            weekend_dates = [first_day + timedelta(days=x) for x in range((last_day-first_day).days + 1) if (first_day + timedelta(days=x)).weekday() == day_name]
            # print(weekend_dates)  
            
            for w_day in weekend_dates:
                # print(w_day.strftime("%d-%m-%Y"))
                if w_day.strftime("%d") not in day_no:
                    day_no.append(w_day.strftime("%d"))
                    out.append({                                                                                                     
                        'title': "Weekend",                                                                                         
                        'id': w_day.strftime("%d"),                                                                                              
                        'start': w_day.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                        'end': w_day.strftime("%m/%d/%Y"),  
                        'color': '#ff8700',                                                           
                    })  
        
        # print(day_no)
                                                                                                                
    return JsonResponse(out, safe=False)  


def attn_more_info(request):
   
    att_id =    request.POST.get('att_id')
    #return HttpResponse(att_id);
    csrf =    request.POST.get('csrfmiddlewaretoken')
    attrn = Attendance.objects.filter(id = att_id)
    jsondata = serializers.serialize('json', attrn)
    return HttpResponse(jsondata, content_type='application/json')
