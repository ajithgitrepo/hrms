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
from app.forms.EmployeeForm import EmployeeForm
from app.models.department_model import Department 

#from app.forms import UserGroupForm  

from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
from app.models.reporting_to_model import Reporting
from django.contrib.auth.models import User
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
import datetime
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.hashers import make_password, check_password


#from app.models import QuillModel



@login_required(login_url="/login/")
def roles(request):
    roles = Group.objects.filter(is_active='1')
   # return HttpResponse("date")
    # print(roles);
    context = {'roles':roles}
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
        Reporting.objects.select_related().filter(employee_id=OuterRef('employee_id')).values('reporting_id')
    ),
    reportee_name=Subquery(
        Employee.objects.filter(employee_id= OuterRef('reporting_id')).values('first_name')
    )
    ).values_list('employee_id', 'first_name', 'reportee_name','pk' )

    # print(query)

    obj = []

    for data in employee:
        reporting = Reporting.objects.filter(employee_id=data.employee_id)
        if reporting:
            reporting_name = Employee.objects.get(employee_id = reporting[0].reporting_id)
            # print(reporting_name.first_name)
            obj.append( { 'employee_id':data.employee_id,'name':data.first_name+' '+data.last_name,'email':data.email_id,'reportee':reporting_name.first_name+' '+reporting_name.last_name, 'role':data.role.name if data.role else None, 'dept': data.department.name if data.department else None  } )
        else:
            obj.append( { 'employee_id':data.employee_id,'name':data.first_name+' '+data.last_name,'email':data.email_id,'reportee':None,  'role':data.role.name if data.role else None, 'dept': data.department.name if data.department else None  } )


    # print(obj)


    context = {'employees':obj}
    return render(request, "employee/index.html", context)

def add_employee(request):  
    
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if  form.is_valid():
            employee_id = request.POST.get('employee_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            # mobile_number = request.POST.get('mobile_number')
            nick_name = request.POST.get('nick_name')
            email_id = request.POST.get('email_id')
            
            department = request.POST.get('department')
            
            reporting_to = request.POST.get('reporting_to')
            source_of_hire = request.POST.get('source_of_hire')
            seating_location = request.POST.get('seating_location')
            location = request.POST.get('location')
            title = request.POST.get('title')
            
            date_of_joining = request.POST.get('date_of_joining')

            date = request.POST.get('date_of_joining')
            if date != "":
               #return HttpResponse(date)
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
            #return HttpResponse(role)
            total_experience = request.POST.get('total_experience')
            experience = request.POST.get('experience')

            other_email = request.POST.get('other_email')

            mobile_phone = request.POST.get('mobile_phone')
            code_name = request.POST.get('code_name')
            code_num = request.POST.get('code_num')

            marital_status = request.POST.get('marital_status')
            #return HttpResponse(marital_status)
           # marital_status = form.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=form.RadioSelect())
            #return HttpResponse(marital_status )
            birth_date = request.POST.get('birth_date')
            
            if birth_date != "":
               d = datetime.datetime.strptime(birth_date, '%d-%m-%Y')
               birth_date = d.strftime('%Y-%m-%d')
            else:
               birth_date = None      
            address = request.POST.get('address')
            tags = request.POST.get('tags')
            #return HttpResponse(address )
            #return HttpResponse(birth_date )

            date_of_exit = request.POST.get('date_of_joining')
            if date_of_exit != "":
               #return HttpResponse(date)
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
                department=department if department else None,
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
                total_experience=total_experience, experience=experience,
                
                other_email=other_email, mobile_phone=mobile_phone,
                marital_status=marital_status, birth_date=birth_date,
                address=address, tags=tags,
                
                job_description=job_description, expertise=expertise,
                about_me=about_me, date_of_exit=date_of_exit, gender=gender,

                ) 
                obj.save()

                latest_id = employee_id           #Employee.objects.latest('id').id

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
                previous_company_name = request.POST.getlist('previous_company_name')
                job_title = request.POST.getlist('job_title')
                from_date = request.POST.getlist('from_date')
                to_date = request.POST.getlist('to_date')
                job_description = request.POST.getlist('job_description')

                #return HttpResponse(from_date)
                #Education
                school_name = request.POST.getlist('school_name')
                degree = request.POST.getlist('degree')
                field = request.POST.getlist('field')
                date_of_completion = request.POST.getlist('date_of_completion')
                interests = request.POST.getlist('interests')

                #Dependent
                dependent_name = request.POST.getlist('dependent_name')
                relationship = request.POST.getlist('relationship')
                date_of_birth = request.POST.getlist('date_of_birth')

                # add work experience details
                c = min([len(previous_company_name), len(job_title), len(from_date), len(to_date), len(job_description)])
               
                for i in range(c):
                        #return HttpResponse(from_date[i])
                    if previous_company_name[i] and job_title[i] and from_date[i] and to_date[i] and job_description[i] :
                        d = datetime.datetime.strptime(from_date[i], '%d-%m-%Y')
                        d2 = datetime.datetime.strptime(to_date[i], '%d-%m-%Y')
                        #return HttpResponse(d)
                        exp = Work_Experience.objects.create(previous_company_name=previous_company_name[i], job_title=job_title[i], from_date= d.strftime('%Y-%m-%d'), to_date=d2.strftime('%Y-%m-%d'), job_description=job_description[i], employee_id= latest_id )
                        #exp.save()
                # return HttpResponse(previous_company_name)        
                # add education details
                c = min([len(school_name), len(degree), len(field), len(date_of_completion), len(interests)])
                
                for i in range(c):
                    if school_name[i] and degree[i] and field[i] and date_of_completion[i] and interests[i] :
                        d = datetime.datetime.strptime(date_of_completion[i], '%d-%m-%Y')
                        edu = Education.objects.create(school_name=school_name[i], degree=degree[i], date_of_completion= d.strftime('%Y-%m-%d'), field=field[i], interests=interests[i], employee_id= latest_id )
                        #edu.save()
                #add dependent details       
                c = min([len(dependent_name), len(relationship), len(date_of_birth)])
                
                for i in range(c):
                    if dependent_name[i] and relationship[i] and date_of_birth[i] :
                        d = datetime.datetime.strptime(date_of_birth[i], '%d-%m-%Y')
                        dept = Dependent.objects.create(dependent_name=dependent_name[i], relationship=relationship[i], date_of_birth= d.strftime('%Y-%m-%d'), employee_id= latest_id )
                        #dept.save()

                if reporting_to !=None:
                    obj = Reporting(
                        created_at=datetime.datetime.now(),
                        updated_at=datetime.datetime.now(),
                        device='web',
                        employee_id=latest_id,
                        reporting_id=reporting_to,
                        updated_by_id=request.user.emp_id,
                        
                    ) 

                    obj.save()

                messages.success(request, first_name + ' Employee was created! ')
                html_template = loader.get_template( 'employee/index.html' )
                #return HttpResponse(html_template.render(request))
                #return render(request, "employees")
                return redirect('employees') 
            else: 
                role = Group.objects.all()
                context_role = {
                        'roles': role,
                       }
          
                context_role.update({"form":form})  
                messages.error(request, ' Employee or EmailID Already Exists! ', context_role)
                context = {'form':form}
                return render(request, "employee/add_employee.html", context)
                
       
    role = Group.objects.filter(is_active = 1)
    department = Department.objects.filter(is_active = 1)
    reporting = Employee.objects.filter(is_active = 1)
    context_role = {
        'roles': role,
        'reporting': reporting,
        'department':department,
    }
   
    #
   # tes = Group.objects.all()
    context_role.update({"form":form})
    return render(request, "employee/add_employee.html",  context_role )
   

def update_employee(request, pk):
    #return HttpResponse('working..')
    #role = Group.objects.get(id=pk)
    employee = Employee.objects.get(employee_id=pk)
    form = EmployeeForm(instance=employee )
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
            
            reporting_to = request.POST.get('reporting_to')
            source_of_hire = request.POST.get('source_of_hire')
            seating_location = request.POST.get('seating_location')
            location = request.POST.get('location')
            title = request.POST.get('title')
            
            date_of_joining = request.POST.get('date_of_joining')

            date = request.POST.get('date_of_joining')
            if date != "":
               #return HttpResponse(date)
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
            #return HttpResponse(role)
            total_experience = request.POST.get('total_experience')
            experience = request.POST.get('experience')

            other_email = request.POST.get('other_email')

            mobile_phone = request.POST.get('mobile_phone')
            code_name = request.POST.get('code_name')
            code_num = request.POST.get('code_num')

            marital_status = request.POST.get('marital_status')
            #return HttpResponse(marital_status)
           # marital_status = form.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=form.RadioSelect())
            #return HttpResponse(marital_status )
            birth_date = request.POST.get('birth_date')
            
            if birth_date != "":
               d = datetime.datetime.strptime(birth_date, '%d-%m-%Y')
               birth_date = d.strftime('%Y-%m-%d')
            else:
               birth_date = None      
            address = request.POST.get('address')
            tags = request.POST.get('tags')
            #return HttpResponse(address )
            #return HttpResponse(birth_date )

            date_of_exit = request.POST.get('date_of_exit')
            if date_of_exit != "":
               #return HttpResponse(date)
               d = datetime.datetime.strptime(date_of_exit, '%d-%m-%Y')
               date_of_exit = d.strftime('%Y-%m-%d')
            else:
               date_of_exit = None 
            gender = request.POST.get('gender')
            about_me = request.POST.get('about_me')
            expertise = request.POST.get('expertise')
            job_description = request.POST.get('job_description')
            #return HttpResponse(pk)
            obj = Employee.objects.filter(employee_id=pk).update(employee_id=employee_id, first_name=first_name, 
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

                ) 

            check_reporting = Reporting.objects.filter(employee_id=pk, is_active = 1)
            

            if check_reporting:
               
               if reporting_to:
                    Reporting.objects.filter(employee_id=pk).update(
                        updated_at=datetime.datetime.now(),
                        employee_id=pk,
                        reporting_id= reporting_to,
                        updated_by_id=request.user.emp_id,
                    )

            else:
                obj = Reporting(
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now(),
                    device='web',
                    employee_id=pk,
                    reporting_id=reporting_to,
                    updated_by_id=request.user.emp_id,
                    
                ) 

                obj.save()


            messages.success(request, ' Employee was updated! ')
            return redirect('employees')

    role = Group.objects.all()
    department = Department.objects.filter(is_active = 1)
    reporting = Employee.objects.filter(is_active = 1).exclude(employee_id = pk)
    reporting_to = Reporting.objects.filter(is_active = 1, employee_id = pk)
    # print(reporting_to[0].employee_id)
    context_role = {
        'roles': role,
        'reporting': reporting,
        'department':department,
        'reporting_to':reporting_to,
    }
    
   # tes = Group.objects.all()
    context_role.update({"form":form, 'employee':employee})
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