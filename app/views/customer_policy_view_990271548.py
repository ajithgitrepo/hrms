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
from app.forms.UserGroupForm import UserGroupForm
from django.utils import timezone
import datetime 
#from app.forms import UserGroupForm   
from app.models.employee_model import Employee 
from app.models.role_model import Role 

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
def index(request):
    
    context = {}
    context['segment'] = 'index' 

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

def customer_policy(request):
    #return HttpResponse('works')
    
     
     """
    
    Employees = Employee.objects.filter(is_active='1', employee_id = emp_id)
    Leave_Types = Leave_Type.objects.filter(is_active='1')
    Leave_Effective_all = Leave_Effective.objects.filter(is_active='1',)
    Leave_Applicable_all = Leave_Applicable.objects.filter(is_active='1', )
    Leave_Restrictions_all = Leave_Restrictions.objects.filter(is_active='1')
    months = 0
    years = 0
    #return HttpResponse(lv_type);

    for each in Employee.objects.filter(is_active='1', employee_id = emp_id):
      emp_name = each.first_name  
      date_of_joing =  each.date_of_joining  
      #return HttpResponse(date_of_joing)
      gender = each.gender
      marital_status = each.marital_status
      department = each.department
     # designation = each.designation
      location = each.location
      role = each.role
      res = ""
      string_res = "" 
      leave_no_of_days = 0

      for each in Leave_Type.objects.filter(is_active='1'):

        leave_type = each.type 
        leave_name = each.name 
        leave_unit = each.unit 
        leave_id = each.id 
        leave_no_of_days = 10 #each.effective_no_of_days 

        for each_effect in Leave_Effective.objects.filter(is_active='1', leave_type_id = leave_id):

            effective_after = each_effect.effective_after
            effective_period = each_effect.effective_period
            effective_from = each_effect.effective_from
            accrual = each_effect.accrual
            accrual_period = each_effect.accrual_period
            effective_on = each_effect.effective_on
            effective_month = each_effect.effective_month
            effective_no_of_days = each_effect.effective_no_of_days
            effective_in = each_effect.effective_in
            reset = each_effect.reset
            reset_period = each_effect.reset_period
            reset_on = each_effect.reset_on
            reset_month = each_effect.reset_month
            reset_carry_forward = each_effect.reset_carry_forward
            reset_carry_forward_max = each_effect.reset_carry_forward_max
            reset_carry_encashment = each_effect.reset_carry_encashment
            reset_carry_method = each_effect.reset_carry_method
            reset_encashment_forward_max = each_effect.reset_encashment_forward_max
            opening_balance = each_effect.opening_balance
            maximum_balance = each_effect.maximum_balance
            reset_carry_count = each_effect.reset_carry_count
            reset_carry_enc_count = each_effect.reset_carry_enc_count
            reset_carry_enc_method = each_effect.reset_carry_enc_method
            reset_carry_forward_overall_limit = each_effect.reset_carry_forward_overall_limit
            reset_carry_forward_expiry_in = each_effect.reset_carry_forward_expiry_in
            reset_carry_forward_expiry_month = each_effect.reset_carry_forward_expiry_month

            for each_applic in Leave_Applicable.objects.filter(is_active='1', leave_type_id = leave_id):

                    exception_dept = each_applic.exception_dept
                    exception_desgn = each_applic.exception_desgn
                    exception_location = each_applic.exception_location
                    exception_role = each_applic.exception_role
                    gender1 = each_applic.gender
                    marital_status1 = each_applic.marital_status
                    department1 = each_applic.department
                    designation1 = each_applic.designation
                    location1 = each_applic.location
                    role1 = each_applic.role
                    #return HttpResponse(each_applic.all_employees)
                    applic = "not_applic";      
                    if each_applic.all_employees == "1":
                        applic = "ok"
                        if  (exception_dept != None) and (exception_role.role == None) :
                          if  (department == exception_dept) or (each_effect.role == exception_role) : 
                             applic = "not_applic"
                    elif (gender1 != None) or (marital_status1 != None) or (department1 != None) or (designation1 != None) or (location1 != None) or (role1 != None) :     
                       applic = "mok"	
                       
                       if str(role) != None and str(role) in str(role1):
                            applic = "ok"
                       if str(gender) != None and str(gender) in str(gender1):
                            applic = "ok"
                       if str(marital_status) != None and str(marital_status) in str(marital_status1):
                            applic = "ok"
                       if str(department) != None and str(department) in str(department1):
                            applic = "ok"	
                      
                    #       applic = "ttttok"	
                    #return HttpResponse(applic)
                    if (applic == "ok") : 
                        #(gender == gender1) or (marital_status == marital_status1) or (department == department1)  or (location == location1) or
                        date1 = datetime.strptime(str(date_of_joing), '%Y-%m-%d')
                        date2 = datetime.strptime(str('2021-08-27'), '%Y-%m-%d')

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

                        leave_no_of_days = each_effect.effective_no_of_days
                        
                        # effective_on = each_effect.effective_on
                        # effective_month = each_effect.effective_month
                        # effective_in = each_effect.effective_on

                
                        if date_of_joing != "": 
                         
                         if accrual == "1":   ####### ACCURAL
                          leave_no_of_days = each_effect.effective_no_of_days
                          
                          
                        if each_effect.accrual_period == "01": # Yearly
                          leave_no_of_days = float(float(each_effect.effective_no_of_days) * years)
                           
 
                        elif each_effect.accrual_period == "00": # One Time
                         leave_no_of_days = float(float(each_effect.effective_no_of_days) * years)
                    
                        elif each_effect.accrual_period == "11":  # monthly
                         leave_no_of_days = float(float(each_effect.effective_no_of_days) * months)
                    #leave_no_of_days = 1

                        elif each_effect.accrual_period == "16":  # half yearly
                            total_month = float(months / 2)
                            leave_no_of_days = float(float(each_effect.effective_no_of_days) * total_month)

                        elif each_effect.accrual_period == "14": # Tri annualy 
                            total_month = float(months / 4)
                            leave_no_of_days = float(float(each_effect.effective_no_of_days) * total_month)

                        elif each_effect.accrual_period == "13": # Quaterly
                            total_month = float(months / 3)
                            leave_no_of_days = float(float(each_effect.effective_no_of_days) * total_month)

                        elif each_effect.accrual_period == "12": # Bi Monthly
                            total_month = float(months / 2)
                            leave_no_of_days = float(float(each_effect.effective_no_of_days) * total_month)
                           
                        elif each_effect.accrual_period == "315":  #Semi Monthly
                         leave_no_of_days = float(float(each_effect.effective_no_of_days) * months)

                        elif (each_effect.accrual_period == "22") or (each_effect.accrual_period == "21"):  #bi Weekly
                            leave_no_of_days = 1 
                            monday1 = (date1 - timedelta(days=date1.weekday()))
                            monday2 = (date2 - timedelta(days=date2.weekday()))
                            week =  (monday2 - monday1).days / 7
                            leave_no_of_days = float(float(each_effect.effective_no_of_days) * week)
                            
                        
                    if reset == "1":    ####### RESET
                        Forward_leave_cont = 0
                        #return HttpResponse(reset_carry_forward) 
                        if reset_carry_method == "0": 
                              Forward_leave_cont = reset_carry_count
                        elif  reset_carry_method == "1":
                              Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100 
                              #print(Forward_leave_cont ) 
                              #return HttpResponse(Forward_leave_cont) 
                        # if reset_carry_forward == "0": # carry forward
                        #     if reset_carry_method == "0": 
                        #      Forward_leave_cont = reset_carry_count
                             
                        #      print(reset_carry_count)
                        #      return HttpResponse(reset_carry_count)
                        #     elif  reset_carry_forward == "1":
                        #      Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100 
                              
                        # elif  reset_carry_forward == "1":
                        #     if reset_carry_method == "0": 
                        #      Forward_leave_cont = reset_carry_count
                        #     elif  reset_carry_forward == "1":
                        #      Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100  

                        # if reset_carry_forward == "1":
                        #     if reset_carry_method == "0": 
                        #      Forward_leave_cont = reset_carry_count
                        #     elif  reset_carry_forward == "1":
                        #      Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100  

                            
                        if each_effect.reset_period == "01": # Yearly  o unit 1 percent
                            #if reset_carry_forward == "1":
                                #reset_max_count = reset_carry_forward_max      
                                # reset_carry_method
                                # reset_carry_count             
                                #float(float(each_effect.effective_no_of_days) * months)
                                #return HttpResponse(Forward_leave_cont)
                                leave_no_of_days = float(float(Forward_leave_cont) * years)
                                
                                
                                #each_effect.effective_no_of_days
                                #return HttpResponse(Forward_leave_cont)
                        elif each_effect.reset_period == "00": # One Time
                            leave_no_of_days = float(float(Forward_leave_cont) * years)

                        elif each_effect.reset_period == "11": # monthly
                            leave_no_of_days = float(float(Forward_leave_cont) * months)

                        elif each_effect.reset_period == "16": # Halfly
                            leave_no_of_days = float(float(Forward_leave_cont) * months / 2)
                        
                        elif each_effect.reset_period == "14": # Triannually
                            leave_no_of_days = float(float(Forward_leave_cont) * months / 3)

                        elif each_effect.reset_period == "13": # Quarterly
                            leave_no_of_days = float(float(Forward_leave_cont) * months / 4)

                        elif each_effect.reset_period == "12": # Bi Monthly
                            leave_no_of_days = float(float(Forward_leave_cont) * months)

                        elif each_effect.reset_period == "315": # Semi Monthly
                            monday1 = (date1 - timedelta(days=date1.weekday()))
                            monday2 = (date2 - timedelta(days=date2.weekday()))
                            week =  (monday2 - monday1).days / 7
                            #leave_no_of_days = float(float(each_effect.effective_no_of_days) * week)
                            leave_no_of_days = float(float(Forward_leave_cont) * week)


                        res = str(res) + str({'name': leave_name, 'type': leave_type, 'unit': leave_unit, 'description': leave_no_of_days, 'id': leave_id}) + (",") 
   
  
      string_res = res.strip(' " " ') #.replace("'","")

    
     Leave_Types =  eval(string_res)
  """
  
     emp_id = request.user.emp_id    #'HRMS 1011' 
    # return HttpResponse(emp_id)
     Employees = Employee.objects.filter(is_active='1')
     Leave_Types = Leave_Balance.objects.filter(is_active='1' , employee_id = emp_id)
     context = {'Leave_Types':Leave_Types, 'Employees': Employees}
     print(context)
    # context_role = {
    #                  'roles': role, 
    #                }
          
    # context_role.update({"form":form}) 
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