# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.models.leave_balance import Leave_Balance
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
from app.models.department_model import *
from app.models.role_model import *
# from app.models import Group 

#from app.models import Group 
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
import MySQLdb
from itertools import chain
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
import datetime

#from app.models import QuillModel

@login_required(login_url="/login/")
def index(request):
    
    leave_types = Leave_Type.objects.filter()

    # print(leave_types)

    context = {
        'leave_types': leave_types,
    } 

    return render(request, "leave/type/index.html",  context )

def add_leave_type(request):  
    
    form = LeaveTypeForm()
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST)
       
        if  form.is_valid():

            name = request.POST.get('name')
            color = request.POST.get('color')
            code = request.POST.get('code')
            types = request.POST.get('type')
            unit = request.POST.get('unit')
            description = request.POST.get('description')
            
            from_date = request.POST.get('from_date')

            date = request.POST.get('from_date')
            if date != "":
               #return HttpResponse(date)
               d = datetime.datetime.strptime(date, "%d-%m-%Y")
               from_date = d.strftime('%Y-%m-%d')
            else:
               from_date = None 

            to_date = request.POST.get('to_date')

            date = request.POST.get('to_date')
            if date != "":
               #return HttpResponse(date)
               d = datetime.datetime.strptime(date, "%d-%m-%Y")
               to_date = d.strftime('%Y-%m-%d')
            else:
               to_date = None 

            if not Leave_Type.objects.filter(Q(name=name)).exists():
                obj = Leave_Type.objects.create(
                    name=name, 
                    color=color,
                    code=code, 
                    type=types,
                    unit=unit,
                    description=description,
                    validity_from=from_date,
                    validity_to=to_date,
                   
                ) 

                obj.save()

                insert_id = Leave_Type.objects.latest('id').id

                gender = request.POST.getlist('gender')
                marital_status = request.POST.getlist('marital_status')
                department = request.POST.getlist('department')
                designation = request.POST.getlist('designation')
                location = request.POST.getlist('location')
                role = request.POST.getlist('role')
                employment_type = request.POST.getlist('employment_type')
                all_employees = request.POST.get('all_employees')
                exception_dept = request.POST.getlist('exception_dept')
                exception_desgn = request.POST.getlist('exception_desgn')
                exception_location = request.POST.getlist('exception_location')
                exception_role = request.POST.getlist('exception_role') 
                exce_employment_type = request.POST.getlist('exce_employment_type')

                remove_square = str(gender)[1:-1]
                remove_single = remove_square.replace("'", "")
                remove_spaces = remove_single.replace(" ", "")

                
              
                if all_employees != None:
                    applicable = Leave_Applicable.objects.create(
                        gender=None, 
                        marital_status=None,
                        department=None, 
                        designation=None,
                        location=None,
                        role=None,
                        employment_type=None,
                        all_employees=all_employees,
                        exception_dept =remove_space(exception_dept),
                        exception_desgn=remove_space(exception_desgn),
                        exception_location=remove_space(exception_location),
                        exception_role=remove_space(exception_role),
                        exception_emp_type=remove_space(exce_employment_type),
                        leave_type_id=insert_id,
                       
                    ) 

              
                if all_employees == None:

                    applicable = Leave_Applicable.objects.create(
                        gender= remove_space(gender), 
                        marital_status=remove_space(marital_status),
                        department=remove_space(department), 
                        designation=remove_space(designation),
                        location=remove_space(location),
                        role=remove_space(role),
                        employment_type=remove_space(employment_type),
                        all_employees=all_employees,
                        exception_dept =remove_space(exception_dept),
                        exception_desgn=remove_space(exception_desgn),
                        exception_location=remove_space(exception_location),
                        exception_role=remove_space(exception_role),
                        exception_emp_type=remove_space(exce_employment_type),
                        leave_type_id=insert_id,
                       
                    )         

                applicable.save()    

                
                effective_after = request.POST.get('effective_after')
                effective_period = request.POST.get('effective_period')
                effective_from = request.POST.get('effective_from')

                accrual = request.POST.get('accrual')
                accrual_period = request.POST.get('accrual_period')
                effective_on = request.POST.get('effective_on')
                effective_month = request.POST.get('effective_month')
                effective_no_of_days = request.POST.get('effective_no_of_days')
                effective_in = request.POST.get('effective_in')

                reset = request.POST.get('reset')
                reset_period = request.POST.get('reset_period')
                reset_on = request.POST.get('reset_on')
                reset_month = request.POST.get('reset_month')
                reset_carry_forward = request.POST.get('reset_carry_forward')
                reset_carry_count = request.POST.get('reset_carry_count')
                reset_carry_method = request.POST.get('reset_carry_method')
                reset_carry_forward_overall_limit = request.POST.get('reset_carry_forward_overall_limit')
                reset_carry_forward_expiry_in=request.POST.get('reset_carry_forward_expiry_in')
                reset_carry_forward_expiry_month=request.POST.get('reset_carry_forward_expiry_month')
                reset_carry_forward_max = request.POST.get('reset_carry_forward_max')
                reset_carry_enc_count = request.POST.get('reset_carry_enc_count')
                reset_carry_enc_method = request.POST.get('reset_carry_enc_method')
                reset_encashment_forward_max = request.POST.get('reset_encashment_forward_max')
                opening_check = request.POST.get('opening_check')
                opening_balance = request.POST.get('opening_balance')
                maximum_check = request.POST.get('maximum_check')
                maximum_balance = request.POST.get('maximum_balance')

                effective = Leave_Effective.objects.create(
                    effective_after=effective_after, 
                    effective_period=effective_period,
                    effective_from=effective_from, 

                    leave_type_id=insert_id,
                   
                )

                effective.save()  
                effective_id = Leave_Effective.objects.latest('id').id

                if accrual != None:
                    obj = Leave_Effective.objects.filter(id=effective_id).update(
                        accrual='1', 
                        accrual_period=accrual_period,
                        effective_on=effective_on, 
                        effective_month=effective_month,
                        effective_no_of_days=effective_no_of_days,
                        effective_in=effective_in,

                    ) 

                if reset != None:
                    obj = Leave_Effective.objects.filter(id=effective_id).update(
                        reset='1', 
                        reset_period=reset_period,
                        reset_on=reset_on, 
                        reset_month=reset_month,
                        reset_carry_forward=reset_carry_forward, 
                        reset_carry_forward_max=reset_carry_forward_max, 
                        reset_carry_method=reset_carry_method, 
                        reset_carry_count=reset_carry_count,
                        reset_carry_forward_overall_limit=reset_carry_forward_overall_limit,
                        reset_carry_forward_expiry_in=reset_carry_forward_expiry_in,
                        reset_carry_forward_expiry_month=reset_carry_forward_expiry_month,
                        reset_carry_enc_count=reset_carry_enc_count,
                        reset_carry_enc_method=reset_carry_enc_method,
                        reset_encashment_forward_max=reset_encashment_forward_max, 
                       
                    ) 

                if opening_check != None:
                    obj = Leave_Effective.objects.filter(id=effective_id).update(
                        opening_balance=opening_balance,
                       
                    )

                if maximum_check != None:
                    obj = Leave_Effective.objects.filter(id=effective_id).update(
                        maximum_balance=maximum_balance,
                       
                    )  


                weekend_bw_leave = request.POST.get('weekend_bw_leave')
                weekend_bw_leave_days = request.POST.get('weekend_bw_leave_days')
                holydays_bw_leave = request.POST.get('holydays_bw_leave')
                holydays_bw_leave_days = request.POST.get('holydays_bw_leave_days')
                exceeds_leave_balance = request.POST.get('exceeds_leave_balance')
                duration = request.POST.get('duration')
                allow_users_to_view = request.POST.get('allow_users_to_view') 
                balance_to_display = request.POST.get('balance_to_display')
                past_dates_check = request.POST.get('past_dates_check')
                past_check = request.POST.get('past_check')
                past_days_count = request.POST.get('past_days_count')
                future_dates_check = request.POST.get('future_dates_check')
                future_check = request.POST.get('future_check')
                future_days_count = request.POST.get('future_days_count')
                future_apply_check = request.POST.get('future_apply_check')
                future_advance_count = request.POST.get('future_advance_count')


                minimum_leave_apply = request.POST.get('minimum_leave_apply')
                maximum_leave_apply = request.POST.get('maximum_leave_apply')
                maximum_consecutive_leave_apply = request.POST.get('maximum_consecutive_leave_apply')
                minimum_gap_apply = request.POST.get('minimum_gap_apply')
                
                file_check = request.POST.get('file_check')
                file_upload_after = request.POST.get('file_upload_after')

                maximum_application = request.POST.get('maximum_application')
                maximum_application_period = request.POST.get('maximum_application_period')

                apply_only_on = request.POST.get('apply_only_on')
                leaves_together = request.POST.get('leaves_together')

                restrictions = Leave_Restrictions.objects.create(
                    weekend_bw_leave=weekend_bw_leave, 
                    weekend_bw_leave_days=weekend_bw_leave_days, 
                    holydays_bw_leave=holydays_bw_leave,
                    holydays_bw_leave_days=holydays_bw_leave_days, 
                    exceeds_leave_balance=exceeds_leave_balance,
                    duration=duration, 
                    allow_users_to_view=allow_users_to_view,
                    balance_to_display=balance_to_display,
                    minimum_leave_apply=minimum_leave_apply, 
                    maximum_leave_apply=maximum_leave_apply,
                    maximum_consecutive_leave_apply=maximum_consecutive_leave_apply, 
                    minimum_gap_apply=minimum_gap_apply,
                    file_upload_after=file_upload_after,
                    maximum_application=maximum_application,
                    maximum_application_period=maximum_application_period,
                    leave_only_on=apply_only_on,
                    leave_cannot_taken_with=leaves_together,
                    leave_type_id=insert_id,
                )

                restrictions.save()  
                restrictions_id = Leave_Restrictions.objects.latest('id').id

                if past_dates_check != None:
                    obj = Leave_Restrictions.objects.filter(id=restrictions_id).update(
                        past_days_count=past_days_count,
                       
                    )

                if future_dates_check != None:
                    obj = Leave_Restrictions.objects.filter(id=restrictions_id).update(
                        leave_request_next_count=future_days_count,
                        leave_request_apply_count=future_advance_count,
                       
                    )

                # Generate Leave Balance

                if all_employees != None:
                    employees = Employee.objects.filter(is_active = '1')
                    
                else:
                   
                    employees = Employee.objects.filter(conditional_gender(gender), conditional_marital(marital_status),conditional_dept(department),conditional_location(location),conditional_role(role),conditional_emp_type(employment_type), is_active = '1').exclude(conditional_exe_dept(exception_dept),conditional_exe_dept(exception_dept),conditional_exe_location(exception_location),conditional_exe_role(exception_role),conditional_exe_emp_type(exce_employment_type))
                    # employees = Employee.objects.raw('SELECT * FROM employee WHERE `gender` IN ('+remove_space+') and is_active = "1" ')
                    # print(employees)


                for emp in employees:

                    today = datetime.datetime.now()
                    end_date = datetime.date.today()
                    start_date = emp.date_of_joining
                    days = end_date - start_date
                    
                    if(effective_period == "1"):
                        years = days.days/365
                        years_count = 0
                        months_count = 0
                        if(years > int(effective_after)):
                            years_count = years - int(effective_after)
                            months_count = years_count * 12

                    if(effective_period == "2"):
                        num_months = int(end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                        months_count = 0
                        years_count = 0
                        if(num_months > int(effective_after)):
                            months_count = num_months - int(effective_after)
                            years_count = months_count / 12

                    if(effective_period == "3"):
                        day_count = 0
                        months_count = 0
                        years_count = 0
                        if(days > int(effective_after)):
                            day_count = days - int(effective_after)
                            months_count = day_count / 30
                            years_count = day_count / 365
                    
                   
                    if accrual != None:

                        effective_no_of_days = int(effective_no_of_days)
                   
                        if accrual_period == "11":
                            balance_count = months_count * effective_no_of_days
                            
                        if accrual_period == "01":
                            balance_count = years_count * effective_no_of_days

                           
                        obj = Leave_Balance.objects.create(
                            balance= balance_count, 
                            device= 'web',
                            employee_id= emp.employee_id, 
                            leave_type_id=insert_id,
                            modified_by_id=request.user.emp_id,
                            is_active= '1',
                        
                        )

                        obj.save()

                messages.success(request, name + ' leave was created! ')
                html_template = loader.get_template( 'leave/type/add_leave_type.html' )
                #return HttpResponse(html_template.render(request))
                #return render(request, "employees")
                return redirect('add_leave_type') 
            else: 
                dept = Department.objects.filter(is_active = '1')
                roles = Group.objects.filter(is_active = '1')
                context = {
                    'dept': dept,
                    'roles': roles,
                }

                context.update({"form":form})
                messages.error(request, 'Leave Type Already Exists!')
                return render(request, "leave/type/add_leave_type.html", context)
          
    dept = Department.objects.filter(is_active = '1')
    roles = Group.objects.filter(is_active = '1')
    context = {
        'dept': dept,
        'roles': roles,
    }

    context.update({"form":form})
    # print(context_role)
    return render(request, "leave/type/add_leave_type.html",  context )


def edit_leave_type(request, pk):  

    dept = Department.objects.filter(is_active = '1')
    roles = Group.objects.filter(is_active = '1')

    leave_type = Leave_Type.objects.get(id = pk)
    effective = leave_type.leave_type_id_effective.get()
    applicable = leave_type.leave_type_id_applicable.get()
    resctrictions = leave_type.leave_type_id_restrictions.get()
    # print(effective.effective_after)

    context = {
        'dept': dept,
        'roles': roles,
        'leave_type': leave_type,
        'effective': effective,
        'applicable': applicable,
        'resctrictions': resctrictions,
    }

    return render(request, "leave/type/edit_leave_type.html",  context )


def edit_leave_type(request, pk):  

    leave_type = Leave_Type.objects.get(id=pk)
    form = LeaveTypeForm(instance=leave_type )

    if request.method == 'POST':
        form = LeaveTypeForm(request.POST, instance=leave_type)
       
        if  form.is_valid():

            name = request.POST.get('name')
            color = request.POST.get('color')
            code = request.POST.get('code')
            types = request.POST.get('type')
            unit = request.POST.get('unit')
            description = request.POST.get('description')
            
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')

            date = request.POST.get('from_date')
            # print(date)
            if date != "":
                #return HttpResponse(date)
                d = datetime.datetime.strptime(date, '%d-%m-%Y')
                from_date = d.strftime('%Y-%m-%d')
            else:
                from_date = None 

            
            date = request.POST.get('to_date')
            if date != "":
                d = datetime.datetime.strptime(date, "%d-%m-%Y")
                to_date = d.strftime('%Y-%m-%d')
            else:
                to_date = None 

            
            type = Leave_Type.objects.filter(id=pk).update(
                name=name, 
                color=color,
                code=code, 
                type=types,
                unit=unit,
                description=description,
                validity_from=from_date,
                validity_to=to_date,

            )

            gender = request.POST.getlist('gender')
            marital_status = request.POST.getlist('marital_status')
            department = request.POST.getlist('department')
            designation = request.POST.getlist('designation')
            location = request.POST.getlist('location')
            role = request.POST.getlist('role')
            employment_type = request.POST.getlist('employment_type')
            all_employees = request.POST.get('all_employees')
            exception_dept = request.POST.getlist('exception_dept')
            exception_desgn = request.POST.getlist('exception_desgn')
            exception_location = request.POST.getlist('exception_location')
            exception_role = request.POST.getlist('exception_role') 
            exce_employment_type = request.POST.getlist('exce_employment_type')

            remove_square = str(gender)[1:-1]
            remove_single = remove_square.replace("'", "")
            remove_spaces = remove_single.replace(" ", "")

            if all_employees != None:
                applicable = Leave_Applicable.objects.filter(leave_type_id=pk).update(
                    gender=None, 
                    marital_status=None,
                    department=None, 
                    designation=None,
                    location=None,
                    role=None,
                    employment_type=None,
                    all_employees=all_employees,
                    exception_dept =remove_space(exception_dept),
                    exception_desgn=remove_space(exception_desgn),
                    exception_location=remove_space(exception_location),
                    exception_role=remove_space(exception_role),
                    exception_emp_type=remove_space(exce_employment_type),

                    
                ) 

            if all_employees == None:
                applicable = Leave_Applicable.objects.filter(leave_type_id=pk).update(
                    gender= remove_space(gender), 
                    marital_status=remove_space(marital_status),
                    department=remove_space(department), 
                    designation=remove_space(designation),
                    location=remove_space(location),
                    role=remove_space(role),
                    employment_type=remove_space(employment_type),
                    all_employees=all_employees,
                    exception_dept =remove_space(exception_dept),
                    exception_desgn=remove_space(exception_desgn),
                    exception_location=remove_space(exception_location),
                    exception_role=remove_space(exception_role),
                    exception_emp_type=remove_space(exce_employment_type),
                    
                )         


            effective_after = request.POST.get('effective_after')
            effective_period = request.POST.get('effective_period')
            effective_from = request.POST.get('effective_from')

            accrual = request.POST.get('accrual')
            accrual_period = request.POST.get('accrual_period')
            effective_on = request.POST.get('effective_on')
            effective_month = request.POST.get('effective_month')
            effective_no_of_days = request.POST.get('effective_no_of_days')
            effective_in = request.POST.get('effective_in')

            reset = request.POST.get('reset')
            reset_period = request.POST.get('reset_period')
            reset_on = request.POST.get('reset_on')
            reset_month = request.POST.get('reset_month')
            reset_carry_forward = request.POST.get('reset_carry_forward')
            reset_carry_count = request.POST.get('reset_carry_count')
            reset_carry_method = request.POST.get('reset_carry_method')
            reset_carry_forward_overall_limit = request.POST.get('reset_carry_forward_overall_limit')
            reset_carry_forward_expiry_in=request.POST.get('reset_carry_forward_expiry_in')
            reset_carry_forward_expiry_month=request.POST.get('reset_carry_forward_expiry_month')
            reset_carry_forward_max = request.POST.get('reset_carry_forward_max')
            reset_carry_enc_count = request.POST.get('reset_carry_enc_count')
            reset_carry_enc_method = request.POST.get('reset_carry_enc_method')
            reset_encashment_forward_max = request.POST.get('reset_encashment_forward_max')
            opening_check = request.POST.get('opening_check')
            opening_balance = request.POST.get('opening_balance')
            maximum_check = request.POST.get('maximum_check')
            maximum_balance = request.POST.get('maximum_balance')

            effective = Leave_Effective.objects.filter(leave_type_id=pk).update(

                effective_after=effective_after, 
                effective_period=effective_period,
                effective_from=effective_from, 

                accrual=accrual, 
                accrual_period=accrual_period,
                effective_on=effective_on, 
                effective_month=effective_month,
                effective_no_of_days=effective_no_of_days,
                effective_in=effective_in,

                reset=reset, 
                reset_period=reset_period,
                reset_on=reset_on, 
                reset_month=reset_month,
                reset_carry_forward=reset_carry_forward, 
                reset_carry_forward_max=reset_carry_forward_max, 
                reset_carry_method=reset_carry_method, 
                reset_carry_count=reset_carry_count,
                reset_carry_forward_overall_limit=reset_carry_forward_overall_limit,
                reset_carry_forward_expiry_in=reset_carry_forward_expiry_in,
                reset_carry_forward_expiry_month=reset_carry_forward_expiry_month,
                reset_carry_enc_count=reset_carry_enc_count,
                reset_carry_enc_method=reset_carry_enc_method,
                reset_encashment_forward_max=reset_encashment_forward_max, 

                opening_balance=opening_balance,
                maximum_balance=maximum_balance,

            )

            weekend_bw_leave = request.POST.get('weekend_bw_leave')
            weekend_bw_leave_days = request.POST.get('weekend_bw_leave_days')
            holydays_bw_leave = request.POST.get('holydays_bw_leave')
            holydays_bw_leave_days = request.POST.get('holydays_bw_leave_days')
            exceeds_leave_balance = request.POST.get('exceeds_leave_balance')
            duration = request.POST.get('duration')
            allow_users_to_view = request.POST.get('allow_users_to_view') 
            balance_to_display = request.POST.get('balance_to_display')
            past_dates_check = request.POST.get('past_dates_check')
            past_check = request.POST.get('past_check')
            past_days_count = request.POST.get('past_days_count')
            future_dates_check = request.POST.get('future_dates_check')
            future_check = request.POST.get('future_check')
            future_days_count = request.POST.get('future_days_count')
            future_apply_check = request.POST.get('future_apply_check')
            future_advance_count = request.POST.get('future_advance_count')


            minimum_leave_apply = request.POST.get('minimum_leave_apply')
            maximum_leave_apply = request.POST.get('maximum_leave_apply')
            maximum_consecutive_leave_apply = request.POST.get('maximum_consecutive_leave_apply')
            minimum_gap_apply = request.POST.get('minimum_gap_apply')
            
            file_check = request.POST.get('file_check')
            file_upload_after = request.POST.get('file_upload_after')

            maximum_application = request.POST.get('maximum_application')
            maximum_application_period = request.POST.get('maximum_application_period')

            apply_only_on = request.POST.get('apply_only_on')
            leaves_together = request.POST.get('leaves_together')

            restrictions = Leave_Restrictions.objects.filter(leave_type_id=pk).update(
                weekend_bw_leave=weekend_bw_leave, 
                weekend_bw_leave_days=weekend_bw_leave_days, 
                holydays_bw_leave=holydays_bw_leave,
                holydays_bw_leave_days=holydays_bw_leave_days, 
                exceeds_leave_balance=exceeds_leave_balance,
                duration=duration, 
                allow_users_to_view=allow_users_to_view,
                balance_to_display=balance_to_display,
                minimum_leave_apply=minimum_leave_apply, 
                maximum_leave_apply=maximum_leave_apply,
                maximum_consecutive_leave_apply=maximum_consecutive_leave_apply, 
                minimum_gap_apply=minimum_gap_apply,
                file_upload_after=file_upload_after,
                maximum_application=maximum_application,
                maximum_application_period=maximum_application_period,
                leave_only_on=apply_only_on,
                leave_cannot_taken_with=leaves_together,
                past_days_count=past_days_count,
                leave_request_next_count=future_days_count,
                leave_request_apply_count=future_advance_count,
            )

            messages.success(request, name + ' Leave type was updated ')
            return redirect('leave_types') 
      
          
    dept = Department.objects.filter(is_active = '1')
    roles = Group.objects.filter(is_active = '1')

    leave_type = Leave_Type.objects.get(id = pk)
    effective = leave_type.leave_type_id_effective.get()
    applicable = leave_type.leave_type_id_applicable.get()
    resctrictions = leave_type.leave_type_id_restrictions.get()
    # print(effective.effective_after)

    context = {
        'dept': dept,
        'roles': roles,
        'leave_type': leave_type,
        'effective': effective,
        'applicable': applicable,
        'resctrictions': resctrictions,
    }

    context.update({"form":form})
    # print(context_role)
    return render(request, "leave/type/edit_leave_type.html",  context )


def conditional_gender(gender):
    if gender:
        return Q(gender__in=gender)
        
    else:
        return Q()

def conditional_marital(marital_status):
    if marital_status:
        return Q(marital_status__in=marital_status)
        
    else:
        return Q()


def conditional_dept(department):
    if department:
        return Q(department__in=department)
        
    else:
        return Q()

def conditional_location(location):
    if location:
        return Q(location__in=location)
        
    else:
        return Q()

def conditional_role(role):
    if role:
        return Q(role__in=role)
        
    else:
        return Q()

def conditional_emp_type(employment_type):
    if employment_type:
        return Q(employee_type__in=employment_type)
        
    else:
        return Q()

def conditional_exe_dept(exception_dept):
    if exception_dept:
        return Q(department__in=exception_dept)
        
    else:
        return Q()

def conditional_exe_location(exception_location):
    if exception_location:
        return Q(location__in=exception_location)
        
    else:
        return Q()

def conditional_exe_role(exception_role):
    if exception_role:
        return Q(role__in=exception_role)
        
    else:
        return Q()

def conditional_exe_emp_type(exce_employment_type):
    if exce_employment_type:
        return Q(employee_type__in=exce_employment_type)
        
    else:
        return Q()


def remove_space(column):
    remove_square = str(column)[1:-1]
    remove_single = remove_square.replace("'", "")
    remove_space = remove_single.replace(" ", "")

    return remove_space


def change_status(request, pk,val):
    data = Leave_Type.objects.get(id=pk)
    data.is_active = val
    data.save()
    messages.success(request,'Leave type status was changed!')
    return redirect('leave_types')