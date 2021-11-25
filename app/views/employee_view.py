

from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.EmployeeForm import EmployeeForm
from app.models.department_model import Department

#from app.forms import UserGroupForm

from app.models.employee_model import Employee, Work_Experience, Education, Dependent
from app.models.reporting_to_model import Reporting
from django.contrib.auth.models import User
# from app.models import Group

#from app.models import Group
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
import MySQLdb
from itertools import chain
import datetime
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.hashers import make_password, check_password

from app.models.leave_type_model import Leave_Type, Leave_Effective, Leave_Applicable, Leave_Restrictions
from app.models.leave_balance_model import Leave_Balance
from dateutil import relativedelta
import os
from django.conf import settings
from app.views.restriction_view import admin_only,role_name




@login_required(login_url="/login/")
def roles(request):
    roles = Group.objects.filter(is_active='1')
   # return HttpResponse("date")
    # print(roles);
    context = {'roles': roles}
    return render(request, "employee/index.html", context)


@login_required(login_url="/login/")
def employees(request):
   # return HttpResponse("employee")
    employee = Employee.objects.select_related().filter(is_active='1')
    # print(employee)

    # test = Employee.objects.select_related().filter(is_active='1')
    # print(test[0].reporting.first_name)

    # report =  Reporting.objects.filter(employee__employee_id__isnull=False)

    # emp =  Employee.objects.filter(reporting__device__contains='web')

    # print(emp)

    # Sub query
    query = Employee.objects.annotate(
        reporting_id=Subquery(
            Reporting.objects.select_related().filter(
                employee_id=OuterRef('employee_id')).values('reporting_id')
        ),
        reportee_name=Subquery(
            Employee.objects.filter(employee_id=OuterRef(
                'reporting_id')).values('first_name')
        )
    ).values_list('employee_id', 'first_name', 'reportee_name', 'pk')

    # print(query)

    obj = []

    for data in employee:
        reporting = Reporting.objects.filter(employee_id=data.employee_id)
        if reporting:
            reporting_name = Employee.objects.get(
                employee_id=reporting[0].reporting_id)
            # print(reporting_name.first_name)
            obj.append({'employee_id': data.employee_id, 'name': data.first_name+' '+data.last_name, 'email': data.email_id, 'reportee': reporting_name.first_name +
                       ' '+reporting_name.last_name, 'role': data.role.name if data.role else None, 'dept': data.department.name if data.department else None})
        else:
            obj.append({'employee_id': data.employee_id, 'name': data.first_name+' '+data.last_name, 'email': data.email_id,
                       'reportee': None,  'role': data.role.name if data.role else None, 'dept': data.department.name if data.department else None})

    # print(obj)

    context = {'employees': obj}
    return render(request, "employee/index.html", context)


def add_employee(request):

    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee_id = request.POST.get('employee_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            # mobile_number = request.POST.get('mobile_number')
            nick_name = request.POST.get('nick_name')
            email_id = request.POST.get('email_id')

            department = request.POST.get('department')

            current_date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            if len(request.FILES) != 0:
                name = os.path.splitext(str(request.FILES['profile']))[0]
                extesion = os.path.splitext(str(request.FILES['profile']))[1]
                handle_uploaded_file(request.FILES['profile'], current_date_time, 'profile_images')
                file_name = name+"-"+current_date_time+""+extesion

                s_name = os.path.splitext(str(request.FILES['signature']))[0]
                s_extesion = os.path.splitext(str(request.FILES['signature']))[1]
                handle_uploaded_file(request.FILES['signature'], current_date_time, 'signature_images')
                s_file_name = s_name+"-"+current_date_time+""+s_extesion

            else:
                file_name = None
                S_file_name = None

            reporting_to = request.POST.get('reporting_to')
            source_of_hire = request.POST.get('source_of_hire')
            seating_location = request.POST.get('seating_location')
            location = request.POST.get('location')
            title = request.POST.get('title')

            date_of_joining = request.POST.get('date_of_joining')

            date = request.POST.get('date_of_joining')
            if date != "":
                # return HttpResponse(date)
                d = datetime.datetime.strptime(date, '%d-%m-%Y')
                date_of_joining = d.strftime('%Y-%m-%d')
            else:
                date_of_joining = None

            #d = datetime.strptime('11/11/2012', '%m/%d/%Y')

            # cr_date = datetime.strptime(date, '%Y-%m-%d')
            #date_of_joining = date.strftime("%Y-%m-%d")
            # d = datetime.strptime(date, '%dd/%mm/%YYYY')
            # date_of_joining = d.strftime('%Y/%m/%d')

            employee_status = request.POST.get('employee_status')
            employee_type = request.POST.get('employee_type')
            work_phone = request.POST.get('work_phone')

            extension = request.POST.get('extension')
            role = request.POST.get('role')

            if role == "":
                role = None
            # return HttpResponse(role)
            total_experience = request.POST.get('total_experience')
            experience = request.POST.get('experience')

            other_email = request.POST.get('other_email')

            mobile_phone = request.POST.get('mobile_phone')
            code_name = request.POST.get('code_name')
            code_num = request.POST.get('code_num')

            marital_status = request.POST.get('marital_status')
            # return HttpResponse(marital_status)
            # marital_status = form.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=form.RadioSelect())
            # return HttpResponse(marital_status )
            birth_date = request.POST.get('birth_date')

            if birth_date != "":
                d = datetime.datetime.strptime(birth_date, '%d-%m-%Y')
                birth_date = d.strftime('%Y-%m-%d')
            else:
                birth_date = None
            address = request.POST.get('address')
            tags = request.POST.get('tags')
            # return HttpResponse(address )
            # return HttpResponse(birth_date )

            date_of_exit = request.POST.get('date_of_joining')
            if date_of_exit != "":
                # return HttpResponse(date)
                d = datetime.datetime.strptime(date_of_exit, '%d-%m-%Y')
                date_of_exit = d.strftime('%Y-%m-%d')
            else:
                date_of_exit = None
            gender = request.POST.get('gender')
            about_me = request.POST.get('about_me')
            expertise = request.POST.get('expertise')
            job_description = request.POST.get('job_description')

            #created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if not Employee.objects.filter(Q(employee_id=employee_id) | Q(email_id=email_id)).exists():
                obj = Employee.objects.create(employee_id=employee_id, first_name=first_name,
                                              last_name=last_name, email_id=email_id, nick_name=nick_name,
                                              department=Department.objects.get(
                                                  id=department) if department else None,
                                              # reporting_to=reporting_to,
                                              source_of_hire=source_of_hire,
                                              seating_location=seating_location,
                                              location=location,
                                              title=title,
                                              date_of_joining=date_of_joining,
                                              employee_status=employee_status,
                                              employee_type=employee_type,
                                              work_phone=work_phone,
                                              code_name=code_name,
                                              code_num=code_num,
                                              extension=extension,
                                              role=Group.objects.get(
                                                  id=role) if role else None,
                                              total_experience=total_experience, experience=experience,

                                              other_email=other_email, mobile_phone=mobile_phone,
                                              marital_status=marital_status, birth_date=birth_date,
                                              address=address, tags=tags,

                                              job_description=job_description, expertise=expertise,
                                              about_me=about_me, date_of_exit=date_of_exit, gender=gender,
                                              profile = file_name,
                                              signature = s_file_name,

                                              )
                # obj.save()

                latest_id = employee_id  # Employee.objects.latest('id').id

                hashed_pwd = make_password("secret")

                obj = User(
                    password=hashed_pwd,
                    is_superuser=1,
                    username=first_name,
                    first_name=first_name,
                    last_name=last_name,
                    email=email_id,
                    role=role,
                    emp_id=latest_id,
                    is_staff=1,
                    is_active=1,
                    date_joined=datetime.datetime.now(),

                )

                obj.save()

                # work experience
                previous_company_name = request.POST.getlist(
                    'previous_company_name')
                job_title = request.POST.getlist('job_title')
                from_date = request.POST.getlist('from_date')
                to_date = request.POST.getlist('to_date')
                job_description = request.POST.getlist('job_description')

                # return HttpResponse(from_date)
                # Education
                school_name = request.POST.getlist('school_name')
                degree = request.POST.getlist('degree')
                field = request.POST.getlist('field')
                date_of_completion = request.POST.getlist('date_of_completion')
                interests = request.POST.getlist('interests')

                # Dependent
                dependent_name = request.POST.getlist('dependent_name')
                relationship = request.POST.getlist('relationship')
                date_of_birth = request.POST.getlist('date_of_birth')

                # add work experience details
                c = min([len(previous_company_name), len(job_title), len(
                    from_date), len(to_date), len(job_description)])

                for i in range(c):
                    # return HttpResponse(from_date[i])
                    if previous_company_name[i] and job_title[i] and from_date[i] and to_date[i] and job_description[i]:
                        d = datetime.datetime.strptime(
                            from_date[i], '%d-%m-%Y')
                        d2 = datetime.datetime.strptime(to_date[i], '%d-%m-%Y')
                        # return HttpResponse(d)
                        exp = Work_Experience.objects.create(previous_company_name=previous_company_name[i], job_title=job_title[i], from_date=d.strftime(
                            '%Y-%m-%d'), to_date=d2.strftime('%Y-%m-%d'), job_description=job_description[i], employee_id=latest_id)
                        # exp.save()
                # return HttpResponse(previous_company_name)
                # add education details
                c = min([len(school_name), len(degree), len(field),
                        len(date_of_completion), len(interests)])

                for i in range(c):
                    if school_name[i] and degree[i] and field[i] and date_of_completion[i] and interests[i]:
                        d = datetime.datetime.strptime(
                            date_of_completion[i], '%d-%m-%Y')
                        edu = Education.objects.create(school_name=school_name[i], degree=degree[i], date_of_completion=d.strftime(
                            '%Y-%m-%d'), field=field[i], interests=interests[i], employee_id=latest_id)
                        # edu.save()
                # add dependent details
                c = min([len(dependent_name), len(
                    relationship), len(date_of_birth)])

                for i in range(c):
                    if dependent_name[i] and relationship[i] and date_of_birth[i]:
                        d = datetime.datetime.strptime(
                            date_of_birth[i], '%d-%m-%Y')
                        dept = Dependent.objects.create(dependent_name=dependent_name[i], relationship=relationship[i], date_of_birth=d.strftime(
                            '%Y-%m-%d'), employee_id=latest_id)
                        # dept.save()

                if reporting_to:
                    obj = Reporting(
                        created_at=datetime.datetime.now(),
                        updated_at=datetime.datetime.now(),
                        device='web',
                        employee_id=latest_id,
                        reporting_id=reporting_to,
                        updated_by_id=request.user.emp_id,

                    )

                    obj.save()

                emp_id = latest_id  # 'HRMS 1011'
                Employees = Employee.objects.filter(
                    is_active='1', employee_id=emp_id)
                Leave_Types = Leave_Type.objects.filter(is_active='1')
                Leave_Effective_all = Leave_Effective.objects.filter(
                    is_active='1',)
                Leave_Applicable_all = Leave_Applicable.objects.filter(
                    is_active='1', )
                Leave_Restrictions_all = Leave_Restrictions.objects.filter(
                    is_active='1')  # no
                months = 0
                years = 0
                if Employees[0].date_of_joining != None:

                    for each in Employee.objects.filter(is_active='1', employee_id=emp_id):

                        emp_name = each.first_name
                        date_of_joing = each.date_of_joining
                        # return HttpResponse(date_of_joing)
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
                                for each_applic in Leave_Applicable.objects.filter(Q(gender=gender1) | Q(gender=None) , is_active='1', leave_type_id=leave_id ):

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
                                        date1 = datetime.datetime.strptime(
                                            str(date_of_joing), '%Y-%m-%d')
                                        dat = datetime.datetime.now().date()
                                        date2 = datetime.datetime.strptime(
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
                                        # effective_on = each_effect.effective_on
                                        # effective_month = each_effect.effective_month
                                        # effective_in = each_effect.effective_on

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
                                        # return HttpResponse(leave_no_of_days)

                                    # if reset == "1":  # RESET
                                    #     # return HttpResponse(reset_carry_method)
                                    #     Forward_leave_cont = 0
                                    #     # return HttpResponse(reset_carry_method)
                                    #     if reset_carry_method == "0":
                                    #         Forward_leave_cont = reset_carry_count
                                    #     elif reset_carry_method == "1":
                                    #         Forward_leave_cont = (
                                    #             float(reset_carry_count) * (years))
                                    #         #print(Forward_leave_cont )
                                    #         # return HttpResponse(Forward_leave_cont)
                                    #     # if reset_carry_forward == "0": # carry forward
                                    #     #     if reset_carry_method == "0":
                                    #     #      Forward_leave_cont = reset_carry_count
                                    #     #      print(reset_carry_count)
                                    #     #      return HttpResponse(reset_carry_count)
                                    #     #     elif  reset_carry_forward == "1":
                                    #     #      Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100
                                    #     # elif  reset_carry_forward == "1":
                                    #     #     if reset_carry_method == "0":
                                    #     #      Forward_leave_cont = reset_carry_count
                                    #     #     elif  reset_carry_forward == "1":
                                    #     #      Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100
                                    #     # if reset_carry_forward == "1":
                                    #     #     if reset_carry_method == "0":
                                    #     #      Forward_leave_cont = reset_carry_count
                                    #     #     elif  reset_carry_forward == "1":
                                    #     #      Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100
                                    #     if each_effect.reset_period == "01":  # Yearly  o unit 1 percent
                                    #         # if reset_carry_forward == "1":
                                    #         #reset_max_count = reset_carry_forward_max
                                    #         # reset_carry_method
                                    #         # reset_carry_count
                                    #         #float(float(each_effect.effective_no_of_days) * months)
                                    #         # return HttpResponse(Forward_leave_cont)
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * years)
                                    #         # return HttpResponse(Forward_leave_cont)
                                    #         # each_effect.effective_no_of_days
                                    #         # return HttpResponse(Forward_leave_cont)
                                    #     elif each_effect.reset_period == "00":  # One Time
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * years)
                                    #     elif each_effect.reset_period == "11":  # monthly
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months)
                                    #     elif each_effect.reset_period == "16":  # Halfly
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months / 2)
                                    #     elif each_effect.reset_period == "14":  # Triannually
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months / 3)
                                    #     elif each_effect.reset_period == "13":  # Quarterly
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months / 4)
                                    #     elif each_effect.reset_period == "12":  # Bi Monthly
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months)
                                    #     elif each_effect.reset_period == "315":  # Semi Monthly
                                    #         monday1 = (
                                    #             date1 - timedelta(days=date1.weekday()))
                                    #         monday2 = (
                                    #             date2 - timedelta(days=date2.weekday()))
                                    #         week = (monday2 - monday1).days / 7
                                    #     #leave_no_of_days = float(float(each_effect.effective_no_of_days) * week)
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * week)
                                    #     # if  Leave_Balance.objects.filter(Q( employee_id=emp_id) and Q(leave_type_id=leave_id)).exists():
                                    #         # return HttpResponse(request.user.emp_id)

                                    balance_leave = Leave_Balance.objects.create(
                                        created_at=timezone.now(),
                                        updated_at=timezone.now(),
                                        modified_at=timezone.now(),
                                        total_month=months,
                                        balance=leave_no_of_days,
                                        employee_id=emp_id,
                                        leave_type_id=leave_id,
                                        device='web',
                                        modified_by_id=request.user.emp_id,
                                    )
                                    balance_leave.save()

                    messages.success(request, first_name +
                                     ' Employee was created! ')
                    html_template = loader.get_template('employee/index.html')
                    # return HttpResponse(html_template.render(request))
                    # return render(request, "employees")
                    return redirect('employees')

                else:
                    emp_id = employee_id  # 'HRMS 1011'
                    # .values_list('date_of_joining', flat=True).first()
                    Employees = Employee.objects.filter(
                        is_active='1', employee_id=emp_id)
                    Leave_Types = Leave_Type.objects.filter(is_active='1')
                    Leave_Effective_all = Leave_Effective.objects.filter(
                        is_active='1',)
                    Leave_Applicable_all = Leave_Applicable.objects.filter(
                        is_active='1', )
                    Leave_Restrictions_all = Leave_Restrictions.objects.filter(
                        is_active='1')  # no
                    months = 0
                    years = 0
                    if Employees[0].date_of_joining != None:
                        for each in Employee.objects.filter(is_active='1', employee_id=emp_id):
                            emp_name = each.first_name
                            date_of_joing = each.date_of_joining
                            # return HttpResponse(date_of_joing)
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

                                    for each_applic in Leave_Applicable.objects.filter(Q(gender=gender1) | Q(gender=None), is_active='1', leave_type_id=leave_id):
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
                                            applic = "ok2"
                                            if(exception_dept != None) and (exception_role.role == None):
                                                if(department == exception_dept) or (each_effect.role == exception_role):
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
                                            date1 = datetime.datetime.strptime(
                                                str(date_of_joing), '%Y-%m-%d')
                                            date2 = datetime.datetime.strptime(
                                                str('2021-10-30'), '%Y-%m-%d')
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
                                            # effective_on = each_effect.effective_on
                                            # effective_month = each_effect.effective_month
                                            # effective_in = each_effect.effective_on

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
                                            # return HttpResponse(leave_no_of_days)
                                        if reset == "1":  # RESET
                                            # return HttpResponse(reset_carry_method)
                                            Forward_leave_cont = 0
                                            # return HttpResponse(reset_carry_method)
                                            if reset_carry_method == "0":
                                                Forward_leave_cont = reset_carry_count
                                            elif reset_carry_method == "1":
                                                Forward_leave_cont = (
                                                    float(reset_carry_count) * (years))
                                                #print(Forward_leave_cont )
                                                # return HttpResponse(Forward_leave_cont)
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
                                            if each_effect.reset_period == "01":  # Yearly  o unit 1 percent
                                                # if reset_carry_forward == "1":
                                                #reset_max_count = reset_carry_forward_max
                                                # reset_carry_method
                                                # reset_carry_count
                                                #float(float(each_effect.effective_no_of_days) * months)
                                                # return HttpResponse(Forward_leave_cont)
                                                leave_no_of_days = float(
                                                    float(Forward_leave_cont) * years)
                                                # return HttpResponse(Forward_leave_cont)
                                                # each_effect.effective_no_of_days
                                                # return HttpResponse(Forward_leave_cont)
                                            elif each_effect.reset_period == "00":  # One Time
                                                leave_no_of_days = float(
                                                float(Forward_leave_cont) * years)
                                            elif each_effect.reset_period == "11":  # monthly
                                                leave_no_of_days = float(
                                                float(Forward_leave_cont) * months)
                                            elif each_effect.reset_period == "16":  # Halfly
                                                leave_no_of_days = float(
                                                float(Forward_leave_cont) * months / 2)
                                            elif each_effect.reset_period == "14":  # Triannually
                                                leave_no_of_days = float(
                                                float(Forward_leave_cont) * months / 3)
                                            elif each_effect.reset_period == "13":  # Quarterly
                                                leave_no_of_days = float(
                                                float(Forward_leave_cont) * months / 4)
                                            elif each_effect.reset_period == "12":  # Bi Monthly
                                                leave_no_of_days = float(
                                                float(Forward_leave_cont) * months)
                                            elif each_effect.reset_period == "315":  # Semi Monthly
                                                monday1 = (
                                                date1 - timedelta(days=date1.weekday()))
                                            monday2 = (
                                                date2 - timedelta(days=date2.weekday()))
                                            week = (monday2 - monday1).days / 7
                                            #leave_no_of_days = float(float(each_effect.effective_no_of_days) * week)
                                            leave_no_of_days = float(
                                                float(Forward_leave_cont) * week)
                                            # if  Leave_Balance.objects.filter(Q( employee_id=emp_id) and Q(leave_type_id=leave_id)).exists():
                                            # return HttpResponse(request.user.emp_id)
                                            balance_leave = Leave_Balance.objects.create(
                                                created_at=timezone.now(),
                                                updated_at=timezone.now(),
                                                modified_at=timezone.now(),
                                                total_month=months,
                                                balance=leave_no_of_days,
                                                employee_id=emp_id,
                                                leave_type_id=leave_id,
                                                type=None,
                                                device='web',
                                                modified_by_id=request.user.emp_id,
                                            )
                                            balance_leave.save()

                    messages.success(request, first_name +' Employee was created! ')
                    html_template = loader.get_template('employee/index.html')
                    # return HttpResponse(html_template.render(request))
                    # return render(request, "employees")
                    return redirect('employees')
            else:
                role = Group.objects.all()
                context_role = {
                    'roles': role,
                }

                context_role.update({"form": form})
                messages.error(
                    request, ' Employee or EmailID Already Exists! ', context_role)
                context = {'form': form}
                return render(request, "employee/add_employee.html", context)

    role = Group.objects.filter(is_active=1)
    department = Department.objects.filter(is_active=1)
    reporting = Employee.objects.filter(
        is_active=1).exclude(employee_id=request.user.emp_id)
    context_role = {
        'roles': role,
        'reporting': reporting,
        'department': department,
    }

    #
   # tes = Group.objects.all()

    context_role.update({"form": form})
    return render(request, "employee/add_employee.html",  context_role)


def handle_uploaded_file(f, current_date_time, folder):
    name = os.path.splitext(str(f))[0]
    extesion = os.path.splitext(str(f))[1]
    file_name = name+"-"+current_date_time+""+extesion
    file_upload_dir = os.path.join(settings.MEDIA_ROOT, folder)
    with open(os.path.join(file_upload_dir, file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def update_employee(request, pk):
   
    employee = Employee.objects.get(employee_id=pk)
    form = EmployeeForm(instance=employee)
    # print(role)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():

            employee_id = request.POST.get('employee_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            # mobile_number = request.POST.get('mobile_number')
            nick_name = request.POST.get('nick_name')
            email_id = request.POST.get('email_id')

            department = request.POST.get('department')

            current_date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            if len(request.FILES) != 0:
                name = os.path.splitext(str(request.FILES['profile']))[0]
                extesion = os.path.splitext(str(request.FILES['profile']))[1]
                handle_uploaded_file(request.FILES['profile'], current_date_time)
                file_name = name+"-"+current_date_time+""+extesion

                s_name = os.path.splitext(str(request.FILES['signature']))[0]
                s_extesion = os.path.splitext(str(request.FILES['signature']))[1]
                handle_uploaded_file(request.FILES['signature'], current_date_time, 'signature_images')
                s_file_name = s_name+"-"+current_date_time+""+s_extesion

            else:
                employee = Employee.objects.get(employee_id = request.user.emp_id)
                # print(employee.profile)
                if employee.profile == None:
                    file_name = None
                else:
                    file_name = employee.profile

                if employee.signature == None:
                    s_file_name = None
                else:
                    s_file_name = employee.signature

            reporting_to = request.POST.get('reporting_to')
            source_of_hire = request.POST.get('source_of_hire')
            seating_location = request.POST.get('seating_location')
            location = request.POST.get('location')
            title = request.POST.get('title')

            date_of_joining = request.POST.get('date_of_joining')

            date = request.POST.get('date_of_joining')
            if date != "":
                # return HttpResponse(date)
                d = datetime.datetime.strptime(date, '%d-%m-%Y')
                date_of_joining = d.strftime('%Y-%m-%d')
            else:
                date_of_joining = None

            #d = datetime.strptime('11/11/2012', '%m/%d/%Y')

            # cr_date = datetime.strptime(date, '%Y-%m-%d')
            #date_of_joining = date.strftime("%Y-%m-%d")
            # d = datetime.strptime(date, '%dd/%mm/%YYYY')
            # date_of_joining = d.strftime('%Y/%m/%d')

            employee_status = request.POST.get('employee_status')
            employee_type = request.POST.get('employee_type')
            work_phone = request.POST.get('work_phone')

            extension = request.POST.get('extension')
            role = request.POST.get('role')

            if role == "":
                role = None
            # return HttpResponse(role)
            total_experience = request.POST.get('total_experience')
            experience = request.POST.get('experience')

            other_email = request.POST.get('other_email')

            mobile_phone = request.POST.get('mobile_phone')
            code_name = request.POST.get('code_name')
            code_num = request.POST.get('code_num')

            marital_status = request.POST.get('marital_status')
            # return HttpResponse(marital_status)
            # marital_status = form.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=form.RadioSelect())
            # return HttpResponse(marital_status )
            birth_date = request.POST.get('birth_date')

            if birth_date != "":
                d = datetime.datetime.strptime(birth_date, '%d-%m-%Y')
                birth_date = d.strftime('%Y-%m-%d')
            else:
                birth_date = None
            address = request.POST.get('address')
            tags = request.POST.get('tags')
            # return HttpResponse(address )
            # return HttpResponse(birth_date )

            date_of_exit = request.POST.get('date_of_exit')
            if date_of_exit != "":
                # return HttpResponse(date)
                d = datetime.datetime.strptime(date_of_exit, '%d-%m-%Y')
                date_of_exit = d.strftime('%Y-%m-%d')
            else:
                date_of_exit = None
            gender = request.POST.get('gender')
            about_me = request.POST.get('about_me')
            expertise = request.POST.get('expertise')
            job_description = request.POST.get('job_description')
            # return HttpResponse(pk)
            obj = Employee.objects.filter(employee_id=pk).update(
                employee_id=employee_id, first_name=first_name,
                last_name=last_name, email_id=email_id, nick_name=nick_name,
                department=department,
                # reporting_to=reporting_to,
                source_of_hire=source_of_hire,
                seating_location=seating_location,
                location=location,
                title=title,
                date_of_joining=date_of_joining,
                employee_status=employee_status,
                employee_type=employee_type,
                work_phone=work_phone,
                code_name=code_name,
                code_num=code_num,
                extension=extension,
                role=role,
                total_experience=total_experience,
                experience=experience,
                other_email=other_email,
                mobile_phone=mobile_phone,
                marital_status=marital_status,
                birth_date=birth_date,
                address=address,
                tags=tags,
                job_description=job_description,
                expertise=expertise,
                about_me=about_me,
                date_of_exit=date_of_exit,
                gender=gender,
                profile=file_name,
                signature=s_file_name,

            )

            check_reporting = Reporting.objects.filter(
                employee_id=pk, is_active=1)

            if check_reporting:

                if reporting_to:
                    Reporting.objects.filter(employee_id=pk).update(
                        updated_at=datetime.datetime.now(),
                        employee_id=pk,
                        reporting_id=reporting_to,
                        updated_by_id=request.user.emp_id,
                    )

            else:
                if reporting_to:
                    obj = Reporting(
                        created_at=datetime.datetime.now(),
                        updated_at=datetime.datetime.now(),
                        device='web',
                        employee_id=pk,
                        reporting_id=reporting_to,
                        updated_by_id=request.user.emp_id,

                    )

                    obj.save()

            if date_of_joining != None:

                if not Leave_Balance.objects.filter(employee_id=employee_id, is_active = 1).exists():

                    for each in Employee.objects.filter(is_active='1', employee_id=employee_id):

                        emp_name = each.first_name
                        date_of_joing = each.date_of_joining
                        # return HttpResponse(date_of_joing)
                        gender = each.gender
                        # print(gender)
                        if not gender:
                            messages.error(request,'Please Update your gender! ')
                            return redirect('profile')
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
                                for each_applic in Leave_Applicable.objects.filter(Q(gender=gender) | Q(gender=None) , is_active='1', leave_type_id=leave_id):

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
                                        date1 = datetime.datetime.strptime(
                                            str(date_of_joing), '%Y-%m-%d')
                                        dat = datetime.datetime.now().date()
                                        date2 = datetime.datetime.strptime(
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
                                        # effective_on = each_effect.effective_on
                                        # effective_month = each_effect.effective_month
                                        # effective_in = each_effect.effective_on

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
                                        # return HttpResponse(leave_no_of_days)

                                    # if reset == "1":  # RESET
                                    #     # return HttpResponse(reset_carry_method)
                                    #     Forward_leave_cont = 0
                                    #     # return HttpResponse(reset_carry_method)
                                    #     if reset_carry_method == "0":
                                    #         Forward_leave_cont = reset_carry_count
                                    #     elif reset_carry_method == "1":
                                    #         Forward_leave_cont = (
                                    #             float(reset_carry_count) * (years))
                                    #         #print(Forward_leave_cont )
                                    #         # return HttpResponse(Forward_leave_cont)
                                    #     # if reset_carry_forward == "0": # carry forward
                                    #     #     if reset_carry_method == "0":
                                    #     #      Forward_leave_cont = reset_carry_count
                                    #     #      print(reset_carry_count)
                                    #     #      return HttpResponse(reset_carry_count)
                                    #     #     elif  reset_carry_forward == "1":
                                    #     #      Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100
                                    #     # elif  reset_carry_forward == "1":
                                    #     #     if reset_carry_method == "0":
                                    #     #      Forward_leave_cont = reset_carry_count
                                    #     #     elif  reset_carry_forward == "1":
                                    #     #      Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100
                                    #     # if reset_carry_forward == "1":
                                    #     #     if reset_carry_method == "0":
                                    #     #      Forward_leave_cont = reset_carry_count
                                    #     #     elif  reset_carry_forward == "1":
                                    #     #      Forward_leave_cont =  float(leave_no_of_days) *  float(reset_carry_count) /100
                                    #     if each_effect.reset_period == "01":  # Yearly  o unit 1 percent
                                    #         # if reset_carry_forward == "1":
                                    #         #reset_max_count = reset_carry_forward_max
                                    #         # reset_carry_method
                                    #         # reset_carry_count
                                    #         #float(float(each_effect.effective_no_of_days) * months)
                                    #         # return HttpResponse(Forward_leave_cont)
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * years)
                                    #         # return HttpResponse(Forward_leave_cont)
                                    #         # each_effect.effective_no_of_days
                                    #         # return HttpResponse(Forward_leave_cont)
                                    #     elif each_effect.reset_period == "00":  # One Time
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * years)
                                    #     elif each_effect.reset_period == "11":  # monthly
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months)
                                    #     elif each_effect.reset_period == "16":  # Halfly
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months / 2)
                                    #     elif each_effect.reset_period == "14":  # Triannually
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months / 3)
                                    #     elif each_effect.reset_period == "13":  # Quarterly
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months / 4)
                                    #     elif each_effect.reset_period == "12":  # Bi Monthly
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * months)
                                    #     elif each_effect.reset_period == "315":  # Semi Monthly
                                    #         monday1 = (
                                    #             date1 - timedelta(days=date1.weekday()))
                                    #         monday2 = (
                                    #             date2 - timedelta(days=date2.weekday()))
                                    #         week = (monday2 - monday1).days / 7
                                    #     #leave_no_of_days = float(float(each_effect.effective_no_of_days) * week)
                                    #         leave_no_of_days = float(
                                    #             float(Forward_leave_cont) * week)
                                    #     # if  Leave_Balance.objects.filter(Q( employee_id=emp_id) and Q(leave_type_id=leave_id)).exists():
                                    #         # return HttpResponse(request.user.emp_id)

                                    balance_leave = Leave_Balance.objects.create(
                                        created_at=timezone.now(),
                                        updated_at=timezone.now(),
                                        modified_at=timezone.now(),
                                        total_month=months,
                                        balance=leave_no_of_days,
                                        employee_id=employee_id,
                                        leave_type_id=leave_id,
                                        device='web',
                                        modified_by_id=request.user.emp_id,
                                    )
                                    balance_leave.save()

                    messages.success(request, first_name + ' Employee profile was updated! ')
                    if role == 'Admin':
                        return redirect('employees')
                    else:
                        return redirect('profile')


            

            role = role_name(request)

            messages.success(request, ' Employee was updated! ')
            
            if role == 'Admin':
                return redirect('employees')
            else:
                return redirect('profile')

    role = Group.objects.all()
    department = Department.objects.filter(is_active=1)
    reporting = Employee.objects.filter(is_active=1).exclude(employee_id=pk)
    reporting_to = Reporting.objects.filter(is_active=1, employee_id=pk)
    # print(reporting)
    context_role = {
        'roles': role,
        'reporting': reporting,
        'department': department,
        'reporting_to': reporting_to,
    }

   # tes = Group.objects.all()
    context_role.update({"form": form, 'employee': employee})
    # print(context_role)
  #  context_role = {'form':form,'employee':employee}
    return render(request, "employee/update_employee.html", context_role)


def delete_employee(request, pk):
    # return HttpResponse('working..')
    data = Employee.objects.get(employee_id=pk)
    data.is_active = 0
    data.save()
    messages.success(request, 'Employee was deleted! ')
    return redirect('employees')
