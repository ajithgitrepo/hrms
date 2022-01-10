from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from app.views.restriction_view import admin_only,role_name
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages 
from django.http import HttpResponseRedirect
from app.forms.UserGroupForm import UserGroupForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm   
from app.models.employee_model import Employee 
from app.models.role_model import Role 
from app.models.reporting_to_model import Reporting
from datetime import datetime, timedelta
from dateutil import relativedelta

from django.core import serializers
from django.http import JsonResponse

from django.contrib.auth.models import Group

from app.models.leave_type_model import Leave_Type, Leave_Effective, Leave_Applicable, Leave_Restrictions 
from app.models.leave_balance_model import Leave_Balance 
from app.models.customized_leave_effective_model import Customize_Leave_Effective 
from django.db.models import Q
from django.db.models import F
from django.db.models import OuterRef, Subquery
from django.db import connection



@login_required(login_url="/login/")
def customer_policy(request):

    role = role_name(request)
    # print(role)
    emp_id = request.user.emp_id 
    if role =="Admin":
        Employees = Employee.objects.filter(is_active='1')
    if role =="Manager":
        Employees = Reporting.objects.select_related().filter(Q(is_active=1) & Q(reporting_id=request.user.emp_id) )
    
    # print(Employees[0].employee.first_name)

    Leave_Types = Leave_Balance.objects.filter(is_active='1', employee_id=emp_id)
    context = {'Leave_Types': Leave_Types, 'Employees': Employees}
    # print(context)

    return render(request, "customer_policy/index.html", context)


def get_custom_leave_type(request):
    
    emp_id =    request.POST.get('emp_id')
    leave_id =    request.POST.get('leave_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
    #result = None
    #if not Customize_Leave_Effective.objects.filter(Q( employee_id = emp_id) and Q(leave_type_id = leave_id )).exists():
    result = Leave_Effective.objects.filter(is_active='1'); #, leave_type_id = leave_id)
    #else:
    # result = Customize_Leave_Effective.objects.filter(is_active='1', leave_type_id = leave_id, employee_id=emp_id)
    
    # final_list = Employee.objects.filter(employee_id = emp_id).annotate(test=Subquery(Group.objects.filter(id = OuterRef('role')).values('role_type')))
    
    jsondata = serializers.serialize('json', result)
    
    return HttpResponse(jsondata, content_type='application/json')

def add_custom_leave_type(request):
      
                #emp_id =    request.POST.get('emp_id')
                leave_id =    request.POST.get('leave_id')
                csrf =    request.POST.get('csrfmiddlewaretoken')
                employee_id = request.POST.get('employee_id')
                
               # effective_after = request.POST.get('effective_after')
               # effective_period = request.POST.get('effective_period')
                effective_from_date = request.POST.get('effective_from_date')

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
                #reset_carry_forward_overall_limit = request.POST.get('reset_carry_forward_overall_limit')
                #reset_carry_forward_expiry_in=request.POST.get('reset_carry_forward_expiry_in')
                #reset_carry_forward_expiry_month=request.POST.get('reset_carry_forward_expiry_month')
                reset_carry_forward_max = request.POST.get('reset_carry_forward_max')
                # reset_carry_enc_count = request.POST.get('reset_carry_enc_count')
                # reset_carry_enc_method = request.POST.get('reset_carry_enc_method')
                # reset_encashment_forward_max = request.POST.get('reset_encashment_forward_max')
                # opening_check = request.POST.get('opening_check')
                # opening_balance = request.POST.get('opening_balance')
                # maximum_check = request.POST.get('maximum_check')
                # maximum_balance = request.POST.get('maximum_balance')

                # print(accrual)
                leave_type_id = request.POST.get('leave_id')
                employee_id = request.POST.get('employee_id')

                status = request.POST.get('status')

                if not Customize_Leave_Effective.objects.filter(Q( employee_id=employee_id) and Q(leave_type_id =leave_type_id)).exists():
                    effective = Customize_Leave_Effective.objects.create(
                       # effective_after=effective_after, 
                       # effective_period=effective_period,
                        effective_from_date=effective_from_date, 
                        employee_id = employee_id,
                        leave_type_id=leave_type_id,
                    )
                    effective.save()
                    
                    obj = Leave_Balance.objects.filter(employee_id=employee_id, leave_type_id =leave_type_id).update(
                       
                        type='CUSTOMIZED', 
                        updated_at=timezone.now() ) 

                    effective_id = Customize_Leave_Effective.objects.latest('id').id
                else:
                    effective_id =  Customize_Leave_Effective.objects.only('id').get(employee_id=employee_id, leave_type_id =leave_type_id).id
                      
                   # print(effective_id)
                if accrual != None:
                    obj = Customize_Leave_Effective.objects.filter(id=effective_id).update(
                        accrual='1', 
                        accrual_period=accrual_period,
                        effective_on=effective_on, 
                        effective_month=effective_month,
                        effective_no_of_days=effective_no_of_days,
                        effective_in=effective_in,
                        effective_from_date=effective_from_date,

                    ) 

                if reset != None:
                    obj = Customize_Leave_Effective.objects.filter(id=effective_id).update(
                        reset='1', 
                        reset_period=reset_period,
                        reset_on=reset_on, 
                        reset_month=reset_month, 
                        reset_carry_forward=reset_carry_forward, 
                        reset_carry_forward_max=reset_carry_forward_max, 
                        reset_carry_method=reset_carry_method, 
                        reset_carry_count=reset_carry_count,
                        #reset_carry_forward_overall_limit=reset_carry_forward_overall_limit,
                        #reset_carry_forward_expiry_in=reset_carry_forward_expiry_in,
                        #reset_carry_forward_expiry_month=reset_carry_forward_expiry_month,
                        #reset_carry_enc_count=reset_carry_enc_count,
                        #reset_carry_enc_method=reset_carry_enc_method,
                        #reset_encashment_forward_max=reset_encashment_forward_max, 
                       
                    )
                   # Calc
                if status == "no_change":   
                    date1 = datetime.strptime(str(effective_from_date), '%Y-%m-%d')
                    current_date = timezone.now().date()
                    #print(current_date)
                    date2 = datetime.strptime(str(current_date), '%Y-%m-%d')

                    difference = relativedelta.relativedelta(date2, date1)
                    #weeks = difference.weeks
                    months = difference.months
                    # add in the number of months (12) for difference in years
                    months += 12 * difference.years
                
                    #months

                    years = difference.years
                    
                    #print(date_of_joing)
                    #print(months)
                    #print(years)
                    #print(weeks)

                    leave_no_of_days = effective_no_of_days
                    
                    # effective_on = each_effect.effective_on
                    # effective_month = each_effect.effective_month
                    # effective_in = each_effect.effective_on

        
                    if date1 != "": 
                        
                      if accrual == "1":   ####### ACCURAL
                        leave_no_of_days = effective_no_of_days
                        
                        
                    if accrual_period == "01": # Yearly
                        leave_no_of_days = float(float(effective_no_of_days) * years)
                        

                    elif accrual_period == "00": # One Time
                        leave_no_of_days = float(float(effective_no_of_days) * years)
                
                    elif accrual_period == "11":  # monthly
                        leave_no_of_days = float(float(effective_no_of_days) * months)
                #leave_no_of_days = 1

                    elif accrual_period == "16":  # half yearly
                        total_month = float(months / 2)
                        leave_no_of_days = float(float(effective_no_of_days) * total_month)

                    elif accrual_period == "14": # Tri annualy 
                        total_month = float(months / 4)
                        leave_no_of_days = float(float(effective_no_of_days) * total_month)

                    elif accrual_period == "13": # Quaterly
                        total_month = float(months / 3)
                        leave_no_of_days = float(float(effective_no_of_days) * total_month)

                    elif accrual_period == "12": # Bi Monthly
                        total_month = float(months / 2)
                        leave_no_of_days = float(float(effective_no_of_days) * total_month)
                        
                    elif accrual_period == "315":  #Semi Monthly
                        leave_no_of_days = float(float(effective_no_of_days) * months)

                    elif (accrual_period == "22") or (accrual_period == "21"):  #bi Weekly
                        leave_no_of_days = 1 
                        monday1 = (date1 - timedelta(days=date1.weekday()))
                        monday2 = (date2 - timedelta(days=date2.weekday()))
                        week =  (monday2 - monday1).days / 7
                        leave_no_of_days = float(float(effective_no_of_days) * week)   
                    print(leave_no_of_days)
                    print(employee_id)
                    print(leave_type_id)
                    obj = Leave_Balance.objects.filter(leave_type_id = leave_type_id, employee_id = employee_id ).update(
                    
                         balance= leave_no_of_days, 
                         updated_at = timezone.now()
                        ) 

               

    # final_list = Employee.objects.filter(employee_id = emp_id).annotate(test=Subquery(Group.objects.filter(id = OuterRef('role')).values('role_type')))
              #  result = Leave_Balance.objects.filter(employee_id = employee_id, is_active = '1').select_related(Leave_Type)
             #   queryset = Leave_Type.objects.filter(id__in = result.values('leave_type_id'))
              #  jsondata = serializers.serialize('json', result)

               # data = Leave_Balance.objects.filter(employee_id = employee_id, is_active = '1').annotate(test=Subquery(Leave_Type.objects.filter(id = OuterRef('leave_type_id')).values('name')))
              #  jsondata = serializers.serialize('json', data)
                cursor = connection.cursor()
                cursor.execute("SELECT lbl.balance ,lbl.type as customtype, lt.name , lt.code , lt.unit , lt.type, lbl.leave_type_id  FROM leave_balance lbl LEFT JOIN leave_type lt ON lbl.leave_type_id = lt.id WHERE lt.is_active='1' and lbl.is_active= '1' and lbl.employee_id = '"+employee_id+"'   ")
                objs = cursor.fetchall()
                json_data = []
                for obj in objs:
                    json_data.append({"balance" : obj[0], "customtype" : obj[1], "name" : obj[2], "code" : obj[3], "unit" : obj[4], "type" : obj[5] , "leave_type_id" : obj[6]})
                return JsonResponse(json_data, safe=False)
              #  return JsonResponse(json_data, safe=False)
                #jsondata = serializers.serialize('json', row)
                #return HttpResponse(row, content_type='application/json')
                #return JsonResponse(row)
                #return jsonify(res)

def get_custom_leave_type_bychange(request):
    
    emp_id =    request.POST.get('employee_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
    #result = None
    
    cursor = connection.cursor()
    cursor.execute("SELECT lbl.balance ,lt.type as customtype, lt.name , lt.code , lt.unit , lt.type, lbl.leave_type_id  FROM leave_balance lbl LEFT JOIN leave_type lt ON lbl.leave_type_id = lt.id WHERE lt.is_active='1' and lbl.is_active= '1' and lbl.employee_id = '"+emp_id+"'   ")
    objs = cursor.fetchall()
    json_data = []

    for obj in objs:
        json_data.append({"balance" : obj[0], "customtype" : obj[1], "name" : obj[2], "code" : obj[3], "unit" : obj[4], "type" : obj[5] , "leave_type_id" : obj[6]})
    
    return JsonResponse(json_data, safe=False)
    
    # final_list = Employee.objects.filter(employee_id = emp_id).annotate(test=Subquery(Group.objects.filter(id = OuterRef('role')).values('role_type')))
    
    #jsondata = serializers.serialize('json', result)
    
    #return HttpResponse(jsondata, content_type='application/json')