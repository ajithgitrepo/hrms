from app.models.location_model import Location
from app.models.leave_type_model import Leave_Type
from app.models.employee_model import Employee
from app.models.leave_type_model import Leave_Effective, Leave_Applicable, Leave_Restrictions
from app.models.leave_balance_model import Leave_Balance
from app.models.attendance_model import Attendance 
import datetime
from datetime import date, time, datetime, timedelta
from dateutil import relativedelta
from django.utils import timezone
import os
from django.db.models import Avg, Count, Min, Sum, Case, When, F
from django.db.models import Q

import random
import string

import logging
logger = logging.getLogger(__name__)


def my_scheduled_job():

    # number = random.choice(string.ascii_letters)
    # number2 = random.choice(string.ascii_letters)
    # Client.objects.create(first_name = number, last_name = number2)
    # # f = open('/Home/thethoughtfactory/Desktop/cron.txt','w')
    # # f.close()

# 	output_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
 
# 	g1 = Location.objects.create(location = output_string, description='description', device='web')

    for each in Leave_Type.objects.filter(is_active='1'):

        leave_id = each.id
        # for eachemp in all_employee:
        for each in Employee.objects.filter(is_active='1'):
            # if not Leave_Balance.objects.filter(employee_id= each.employee_id, is_active = 1).exists():
            if each.date_of_joining != None:
                emp_name = each.first_name
                date_of_joing = each.date_of_joining
            # return HttpResponse(date_of_joing)
                gender = each.gender
                marital_status = each.marital_status
                department = each.department
                # designation = each.designation
                location = each.location_id
                role = each.role
                res = ""
                string_res = ""
                leave_no_of_days = 0
                for eachlv in Leave_Type.objects.filter(is_active='1'):
                    leave_type = eachlv.type
                    leave_name = eachlv.name
                    leave_unit = eachlv.unit
                    leave_id = eachlv.id
                # leave_no_of_days = each.effective_no_of_days  # Number Of Leaves
                    for each_effect in Leave_Effective.objects.filter(is_active='1', leave_type_id=leave_id):
                        # return HttpResponse(each_effect.effective_after)
                        effective_after = each_effect.effective_after
                        effective_period = each_effect.effective_period
                        effective_from = each_effect.effective_from
                        accrual = each_effect.accrual
                        accrual_period = each_effect.accrual_period
                        effective_on = each_effect.effective_on
                        effective_month = each_effect.effective_month
                        effective_no_of_days = each_effect.effective_no_of_days
                        # logger.warning(effective_no_of_days)
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
                        for each_applic in Leave_Applicable.objects.filter(Q(gender=gender) | Q(gender=None), is_active='1', leave_type_id=leave_id):
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
                            # return HttpResponse(gender1)
                            applic = "not_applic"
                            if each_applic.all_employees == "1":
                                applic = "ok"
                                if (exception_dept != None) and (exception_role != None):
                                    if (department == exception_dept) or (each_applic.role == exception_role):
                                        applic = "not_applic"
                            elif (gender1 != None) or (marital_status1 != None) or (department1 != None) or (designation1 != None) or (location1 != None) or (role1 != None):
                                applic = "mok"
                                if str(role) != None and str(role) in str(role1):
                                    applic = "ok"
                                if str(gender) != None and (str(gender) in str(gender1)):
                                    applic = "ok"
                                if str(marital_status) != None and str(marital_status) in str(marital_status1):
                                    applic = "ok"
                                if str(department) != None and str(department) in str(department1):
                                    applic = "ok"
                            #       applic = "ttttok"
                            # return HttpResponse(applic)
                            if (applic == "ok"):
                                # (gender == gender1) or (marital_status == marital_status1) or (department == department1)  or (location == location1) or
                                # return HttpResponse(date_of_joing)
                                date1 = datetime.strptime(
                                    str(date_of_joing), '%Y-%m-%d')
                                dat = datetime.now().date()
                                date2 = datetime.strptime(
                                    str(dat), '%Y-%m-%d')
                                difference = relativedelta.relativedelta(
                                    date2, date1)
                                #weeks = difference.weeks
                                months = difference.months
                                # add in the number of months (12) for difference in years
                                months += 12 * difference.years
                                # months
                                years = difference.years
                                # return HttpResponse(months)
                                leave_no_of_days = each_effect.effective_no_of_days
                                # logger.warning(leave_no_of_days)

                                if date_of_joing != "":
                                    if accrual == "1":  # ACCURAL
                                        leave_no_of_days = each_effect.effective_no_of_days
                                # return HttpResponse(each_effect.accrual_period)
                                    if each_effect.accrual_period == "01":  # Yearly
                                        leave_no_of_days = float(
                                            float(each_effect.effective_no_of_days) * years)
                                    elif each_effect.accrual_period == "00":  # One Time
                                        leave_no_of_days = each_effect.effective_no_of_days
                                # float(float(each_effect.effective_no_of_days) * years)
                                    elif each_effect.accrual_period == "11":  # monthly
                                        leave_no_of_days = float(
                                            float(each_effect.effective_no_of_days) * months)
                                #leave_no_of_days = 1
                                    elif each_effect.accrual_period == "16":  # half yearly
                                        total_month = float(months / 2)
                                        leave_no_of_days = float(
                                            float(each_effect.effective_no_of_days) * total_month)
                                elif each_effect.accrual_period == "14":  # Tri annualy
                                    total_month = float(months / 4)
                                    leave_no_of_days = float(
                                        float(each_effect.effective_no_of_days) * total_month)
                                elif each_effect.accrual_period == "13":  # Quaterly
                                    total_month = float(months / 3)
                                    leave_no_of_days = float(
                                        float(each_effect.effective_no_of_days) * total_month)
                                elif each_effect.accrual_period == "12":  # Bi Monthly
                                    total_month = float(months / 2)
                                    leave_no_of_days = float(
                                        float(each_effect.effective_no_of_days) * total_month)
                                elif each_effect.accrual_period == "315":  # Semi Monthly
                                    leave_no_of_days = float(
                                        float(each_effect.effective_no_of_days) * months)
                                # bi Weekly
                                elif (each_effect.accrual_period == "22") or (each_effect.accrual_period == "21"):
                                    leave_no_of_days = 1
                                    monday1 = (
                                        date1 - timedelta(days=date1.weekday()))
                                    monday2 = (
                                        date2 - timedelta(days=date2.weekday()))
                                    week = (monday2 - monday1).days / 7
                                    leave_no_of_days = float(
                                        float(each_effect.effective_no_of_days) * week)
                                    # logger.warning(leave_no_of_days)
    
                                
                                if not Leave_Balance.objects.filter(employee_id=each.employee_id, leave_type_id=leave_id, is_active=1).exists():
                                    # return HttpResponse(each.employee_id)
                                    # logger.warning('dfg')
                                    balance_leave = Leave_Balance.objects.create(
                                        created_at=timezone.now(),
                                        updated_at=timezone.now(),
                                        modified_at=timezone.now(),
                                        total_month=months,
                                        balance=leave_no_of_days,
                                        employee_id=each.employee_id,
                                        leave_type_id=leave_id,
                                        device='web',
                                        modified_by_id='Emp001',
                                        
                                    )
                                else:
                                   # return HttpResponse('dd')
                                    tot = Leave_Balance.objects.filter(
                                        employee_id=each.employee_id, leave_type_id=leave_id, is_active=1)
                                    tot_month = tot[0].total_month
                                    # logger.warning(tot_month)
                                    # logger.warning('dfgh')
                                    

                                    date1 = datetime.strptime(str(date_of_joing), '%Y-%m-%d')
                                    dat = datetime.now().date()
                                    date2 = datetime.strptime(
                                        str(dat), '%Y-%m-%d')

                                    month_count = date2.month - date1.month
                                    # logger.warning('month_count')-logger.warning(month_count)         
                                    # logger.warning(month_count)
                                    # return HttpResponse(month_count) 
                                    if month_count < 0:
                                        # logger.warning('coming')

                                        month_count = 0
                                    else:
                                        # logger.warning(leave_no_of_days)
                                        # return HttpResponse(months)
                                        if(str(tot_month) >= str(effective_after)):
                                          
                                            Leave_Balance.objects.filter(employee_id=each.employee_id, leave_type_id=leave_id).update(
                                                balance=F(
                                                    "balance") + leave_no_of_days,
                                                total_month=month_count,
                                                #  type='CUSTOMIZED',
                                                updated_at=timezone.now()
                                                

                                            )
                                            logger.warning('Leave Balance cron  run at '+str(datetime.now())+' hours!')

def checkout():
    myDate = datetime.now()
    attn = Attendance.objects.filter(is_active = 1,  date = myDate, is_present = 1, checkin_active = 1, checkout_active = 0 )
    # print(attn)

    for att in attn:
        Attendance.objects.filter(id = att.id ).update(
            checkout_time = datetime.now().strftime('%H:%M:%S'),
            updated_at = datetime.now(),
            checkout_active=1, 
        )
    
    logger.warning('Attendance cron run at '+str(datetime.now())+' hours!')
	
	