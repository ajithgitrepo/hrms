
from django import http
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.utils import timezone
from app.models import weekend_model
from app.models.employee_model import Employee
from app.models.holiday_details_model import Holiday_Detail 
from app.models.weekend_model import Weekend
import datetime 
from datetime import datetime, timedelta
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


#from app.models import QuillModel


@login_required(login_url="/login/")
def index(request):
   
    context = {}
    context['segment'] = 'index' 

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

def check_in_attn(request):
    if request.method == 'POST':
        myDate = datetime.now()
        if not Attendance.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, checkin_time__isnull=False)).exists():
            insert = Attendance.objects.create(date=myDate, checkin_time=datetime.now().strftime('%H:%M:%S'), employee_id= request.user.emp_id)
            request.session['checkin_session'] = datetime.now().strftime('%H:%M:%S')
            if not Attendance.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, is_leave=1)).exists():
                update = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id ).update(
                    is_present = 1,
                )
            messages.success(request,' Checked in successfully ')
            return redirect('home')
        else:
            update = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id ).update(
                updated_at = datetime.now(),
            )
            request.session['checkin_session'] = datetime.now().strftime('%H:%M:%S')
            # print(request.session['checkin_session'])

    return redirect('home')

def check_out_attn(request):
    if request.method == 'POST':
        myDate = datetime.now()
        if Attendance.objects.filter(Q(employee_id=request.user.emp_id, date=myDate, checkin_time__isnull=False)).exists():
            update = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id ).update(
                checkout_time = datetime.now().strftime('%H:%M:%S'),
                updated_at = datetime.now(),
            )
            del request.session['checkin_session']
            messages.success(request,' Checked out successfully ')
            return redirect('home')

        else:
            del request.session['checkin_session']
            messages.success(request,' Checked out successfully ')
            return redirect('home')

    return redirect('home')


def attn_listview(request):

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

    print(dates)

    month_atten = Attendance.objects.filter(is_active = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day])
    # print(month_atten)

    present_days = Attendance.objects.filter(is_active = 1, is_present = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(present_days)

    absent_days = Attendance.objects.filter(is_active = 1, is_leave = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(absent_days)

    zipped_data = zip(dates, date_no)
    # print(date_no)
    employees = Employee.objects.filter(is_active = 1)

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
    # print(present_days)

    absent_days = Attendance.objects.filter(is_active = 1, is_leave = 1, employee_id = pk, date__range=[first_day, last_day]).count()
    # print(absent_days)

    holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 
 
 
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
    # print(present_days)

    absent_days = Attendance.objects.filter(is_active = 1, is_leave = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day]).count()
    # print(absent_days)

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
    # print(present_days)

    absent_days = Attendance.objects.filter(is_active = 1, is_leave = 1, employee_id = pk, date__range=[first_day, last_day]).count()
    # print(absent_days)

    holidays = Holiday_Detail.objects.filter(is_active = 1, date__range=[first_day, last_day]) 
 

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
    }
    

    return render(request, "attendance/attn_tabular.html",context)

def export_excel(request):
        
        # create a workbook in memory
        output = BytesIO()

        # now = datetime.now()
        # current_year = datetime.now().strftime("%Y")
        # current_month = datetime.now().strftime("%m")
        # month_year = current_month+'-'+current_year
        # first_day = now.replace(day = 1)
        # last_day = now.replace(day = calendar.monthrange(now.year, now.month)[1])

        # month_number = datetime.datetime.strptime(request.POST.get('month'), "%b")
        
        date = datetime.strptime(request.POST.get('month'), "%m-%Y")
        first_day = date.replace(day = 1)
        last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])

        book = xlsxwriter.Workbook(output)
        sheet = book.add_worksheet('test')
        sheet.set_column(0, 5, 25)
        
        # Set up some formats to use.
        bold = book.add_format({'bold': True})

        sheet.write('A1', 'Employee Id', bold)
        sheet.write('B1', 'Employee Name', bold)
        sheet.write('C1', 'Date', bold)
        sheet.write('D1', 'First Check-In', bold)
        sheet.write('E1', 'First Check-Out', bold)
        sheet.write('F1', 'Check-In Location', bold)


        month_atten = Attendance.objects.filter(is_active = 1,  employee_id = request.POST.get('employee_id'), employee__is_active = 1, date__range=[first_day, last_day])
        # print(month_atten)

        row_num = 2
        for row_data in month_atten.iterator():
            # print(row_data.employee.first_name)
            # sheet.write_row(row_num, 0, row_data)
            sheet.write('A'+str(row_num), row_data.employee.employee_id)
            sheet.write('B'+str(row_num), row_data.employee.first_name +" "+row_data.employee.last_name)
            sheet.write('C'+str(row_num), (row_data.date).strftime("%d-%m-%Y"))
            sheet.write('D'+str(row_num), (row_data.checkin_time ).strftime("%I:%M%p") if row_data.checkin_time else "-" )
            sheet.write('E'+str(row_num), (row_data.checkout_time).strftime("%I:%M%p") if row_data.checkout_time else "-" )
           
            row_num += 1

        book.close()

        output.seek(0)

        # Set up the Http response.
        filename = month_atten[0].employee.first_name+'-'+str(request.POST.get('month'))+'.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

def attn_calendarview(request):

    employees = Employee.objects.filter(is_active = 1)

    context = {
        "employees":employees,
    }

    return render(request, "attendance/attn_calendar.html",context)


def show_cal_view(request):   
    #return HttpResponse('work')  

    date = datetime.now()
    # print(now)
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    month_year = current_month+'-'+current_year
    
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])

    month_atten = Attendance.objects.filter(is_active = 1, employee_id = request.user.emp_id, date__range=[first_day, last_day])
    # print(month_atten)
    
    all_holidays = Holiday_Detail.objects.filter(is_active = 1) 
                                                                                       
    out = []                                                                                                             
    for attn in month_atten:     
        if attn.is_present == 1:
            out.append({                                                                                                     
                'title': 'Present',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#3dce4cd9',                                                           
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
    #return HttpResponse(out)                                                                                                                   
    return JsonResponse(out, safe=False)  


def show_attn_time(request):
    id = request.GET.get("id", None)
    data = Attendance.objects.filter(id=id)
    tmpJson = serializers.serialize("json",data)
    tmpObj = json.loads(tmpJson)
    
    return JsonResponse(tmpObj, safe=False)



def search_attn_time(request):   

    emp_id = request.GET.get("emp_id", None)

    date = datetime.now()
    # print(now)
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    month_year = current_month+'-'+current_year
    
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])

    month_atten = Attendance.objects.filter(is_active = 1, employee_id = emp_id, date__range=[first_day, last_day])
    # print(month_atten)
    
    all_holidays = Holiday_Detail.objects.filter(is_active = 1) 
                                                                                       
    out = []                                                                                                             
    for attn in month_atten:     
        if attn.is_present == 1:
            out.append({                                                                                                     
                'title': 'Present',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#2fb136',                                                           
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

    return JsonResponse(out, safe=False)  


def search_attn_date(request):   

    date = request.GET.get("date")
    emp_id = request.GET.get("emp_id")
   
    date_c = datetime.strptime(date, "%m/%d/%Y")
    first_day = date_c.replace(day = 1)
    last_day = date_c.replace(day = calendar.monthrange(date_c.year, date_c.month)[1])
    print(first_day)
    
    month_atten = Attendance.objects.filter(is_active = 1, employee_id = emp_id, date__range=[first_day, last_day])
    
    all_holidays = Holiday_Detail.objects.filter(is_active = 1) 
                                                                                       
    out = []                                                                                                             
    for attn in month_atten:     
        if attn.is_present == 1:
            out.append({                                                                                                     
                'title': 'Present',                                                                                         
                'id': attn.id,                                                                                              
                'start': attn.date.strftime("%m/%d/%Y"),    #, %H:%M:%S                                                      
                'end': attn.date.strftime("%m/%d/%Y"),  
                'checkin': attn.checkin_time.strftime("%H:%M:%S") if attn.checkin_time else "None",
                'checkout': attn.checkout_time.strftime("%H:%M:%S") if attn.checkout_time else "None", 
                'color': '#2fb136',                                                           
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
            'color': '#ff1a1a',                                                           
        })          
                                                                                                                        
    return JsonResponse(out, safe=False)  