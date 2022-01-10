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
# from app.EmployeeForm import EmployeeForm 
#from app.forms import UserGroupForm  

# from app.models import Employee 
# from app.models import Group 

#from app.models import Group 
from django.conf.urls import url
from pprint import pprint
from datetime import datetime
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


#from app.models import QuillModel



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

# def snippets(request):
#     roles = Group.objects.filter(is_active='1')
#     emp_id =    request.POST.get('emp_id')
#     csrf =    request.POST.get('csrfmiddlewaretoken')
#     employee = Employee.objects.filter(employee_id = emp_id)#.prefetch_related('id')
#     roles = Group.objects.filter(is_active='1') 
#     final_list = list(chain(employee, roles)) 
#     #final_list = Employee.objects.filter(roles).values_list('name', flat=True)
#     #final_list =  Employee.objects.raw('select * from auth_group where  id = 3')
#     #final_list = Employee.objects.all().prefetch_related(Prefetch('id', queryset=Group.objects.filter(is_active='1')))
#     #print(final_list)
#     jsondata = serializers.serialize('json', final_list)
    
# #     sql = "SELECT * FROM employee AS emp JOIN auth_group AS grp ON emp.role = grp.id" 
# #     cursor = connection.cursor()
# #     cursor.execute(sql, ['localhost'])
# #     row = cursor.fetchall()
    
# #     print(row)
# #     return HttpResponse(sql)
#     return HttpResponse(jsondata, content_type='application/json')
#    # result = serializers.serialize('json', [employee,])
#    # return HttpResponse(employee) #WHERE #a.name = %s
# #     return HttpResponse(test)
# #     print(roles);
# #     context = {'roles':roles} 
# #     return render(request, "employee/index.html", context)

# def update_employee(request, pk):
#     #return HttpResponse('working..')
#     #role = Group.objects.get(id=pk)
#     employee = Employee.objects.get(id=pk)
#     form = EmployeeForm(instance=employee )
#     # print(role)
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST, instance=employee)
#         if form.is_valid():
            
#             employee_id = request.POST.get('employee_id')
#             first_name = request.POST.get('first_name')
#             last_name = request.POST.get('last_name')
#             # mobile_number = request.POST.get('mobile_number')
#             nick_name = request.POST.get('nick_name')
#             email_id = request.POST.get('email_id')
            
#             department = request.POST.get('department')
            
#             reporting_to = request.POST.get('reporting_to')
#             source_of_hire = request.POST.get('source_of_hire')
#             seating_location = request.POST.get('seating_location')
#             location = request.POST.get('location')
#             title = request.POST.get('title')
            
#             date_of_joining = request.POST.get('date_of_joining')

#             date = request.POST.get('date_of_joining')
#             if date != "":
#                #return HttpResponse(date)
#                d = datetime.strptime(date, '%d-%m-%Y')
#                date_of_joining = d.strftime('%Y-%m-%d')
#             else:
#                date_of_joining = None 
             
#             #d = datetime.strptime('11/11/2012', '%m/%d/%Y')
            
#            # cr_date = datetime.strptime(date, '%Y-%m-%d')
#             #date_of_joining = date.strftime("%Y-%m-%d")
#            # d = datetime.strptime(date, '%dd/%mm/%YYYY')
#            # date_of_joining = d.strftime('%Y/%m/%d')

#             employee_status = request.POST.get('employee_status')
#             employee_type = request.POST.get('employee_type')
#             work_phone = request.POST.get('work_phone')

#             extension = request.POST.get('extension')
#             role = request.POST.get('role')
            
#             if role == "":
#                   role = None
#             #return HttpResponse(role)
#             total_experience = request.POST.get('total_experience')
#             experience = request.POST.get('experience')

#             other_email = request.POST.get('other_email')

#             mobile_phone = request.POST.get('mobile_phone')
#             code_name = request.POST.get('code_name')
#             code_num = request.POST.get('code_num')

#             marital_status = request.POST.get('marital_status')
#             #return HttpResponse(marital_status)
#            # marital_status = form.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=form.RadioSelect())
#             #return HttpResponse(marital_status )
#             birth_date = request.POST.get('birth_date')
            
#             if birth_date != "":
#                d = datetime.strptime(birth_date, '%d-%m-%Y')
#                birth_date = d.strftime('%Y-%m-%d')
#             else:
#                birth_date = None      
#             address = request.POST.get('address')
#             tags = request.POST.get('tags')
#             #return HttpResponse(address )
#             #return HttpResponse(birth_date )

#             date_of_exit = request.POST.get('date_of_joining')
#             if date_of_exit != "":
#                #return HttpResponse(date)
#                d = datetime.strptime(date_of_exit, '%d-%m-%Y')
#                date_of_exit = d.strftime('%Y-%m-%d')
#             else:
#                date_of_exit = None 
#             gender = request.POST.get('gender')
#             about_me = request.POST.get('about_me')
#             expertise = request.POST.get('expertise')
#             job_description = request.POST.get('job_description')
#             #return HttpResponse(pk)
#             obj = Employee.objects.filter(id=pk).update(employee_id=employee_id, first_name=first_name, 
#                 last_name=last_name, email_id=email_id, nick_name=nick_name,
#                 department=department,
#                 reporting_to=reporting_to,
#                 source_of_hire=source_of_hire,
#                 seating_location=seating_location,
#                 location=location,
#                 title=title,
#                 date_of_joining=date_of_joining,
#                 employee_status=employee_status,
#                 employee_type=employee_type,
#                 work_phone=work_phone,
#                 code_name=code_name,
#                 code_num=code_num,
#                 extension=extension,
#                 role=role,
#                 total_experience=total_experience, experience=experience,
                
#                 other_email=other_email, mobile_phone=mobile_phone,
#                 marital_status=marital_status, birth_date=birth_date,
#                 address=address, tags=tags,
                
#                 job_description=job_description, expertise=expertise,
#                 about_me=about_me, date_of_exit=date_of_exit, gender=gender,

#                 ) 
#            # obj.save()

#             #employee.save()
#             #form.save()
#             messages.success(request, ' Role was updated! ')
#             return redirect('employees')
#     role = Group.objects.all()
#     context_role = {
#           'roles': role,
#          #  'country': 'in'
#        }
    
#    # tes = Group.objects.all()
#     context_role.update({"form":form, 'employee':employee})
#     print(context_role)
#   #  context_role = {'form':form,'employee':employee}
#     return render(request, "employee/update_employee.html", context_role)

# def delete_employee(request, pk):
#     # return HttpResponse('working..')
#     data = Employee.objects.get(id=pk)
#     data.is_active = 0
#     data.save()
#     messages.success(request, 'Employee was deleted! ')
#     return redirect('employees')

# def roles(request):
#     roles = Group.objects.filter(is_active='1')
#    # return HttpResponse("date")
#     print(roles);
#     context = {'roles':roles}
#     return render(request, "employee/index.html", context)

# def employees(request):
#     employee = Employee.objects.filter(is_active='1')
#     #return HttpResponse(employee)
#     print(employee);
#     context = {'employees':employee}
#     return render(request, "employee/index.html", context)

# def add_employee(request):  
    
#     form = EmployeeForm()
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
#         if  form.is_valid():
#             employee_id = request.POST.get('employee_id')
#             first_name = request.POST.get('first_name')
#             last_name = request.POST.get('last_name')
#             # mobile_number = request.POST.get('mobile_number')
#             nick_name = request.POST.get('nick_name')
#             email_id = request.POST.get('email_id')
            
#             department = request.POST.get('department')
            
#             reporting_to = request.POST.get('reporting_to')
#             source_of_hire = request.POST.get('source_of_hire')
#             seating_location = request.POST.get('seating_location')
#             location = request.POST.get('location')
#             title = request.POST.get('title')
            
#             date_of_joining = request.POST.get('date_of_joining')

#             date = request.POST.get('date_of_joining')
#             if date != "":
#                #return HttpResponse(date)
#                d = datetime.strptime(date, '%d-%m-%Y')
#                date_of_joining = d.strftime('%Y-%m-%d')
#             else:
#                date_of_joining = None 
             
#             #d = datetime.strptime('11/11/2012', '%m/%d/%Y')
            
#            # cr_date = datetime.strptime(date, '%Y-%m-%d')
#             #date_of_joining = date.strftime("%Y-%m-%d")
#            # d = datetime.strptime(date, '%dd/%mm/%YYYY')
#            # date_of_joining = d.strftime('%Y/%m/%d')

#             employee_status = request.POST.get('employee_status')
#             employee_type = request.POST.get('employee_type')
#             work_phone = request.POST.get('work_phone')

#             extension = request.POST.get('extension')
#             role = request.POST.get('role')
            
#             if role == "":
#                   role = None
#             #return HttpResponse(role)
#             total_experience = request.POST.get('total_experience')
#             experience = request.POST.get('experience')

#             other_email = request.POST.get('other_email')

#             mobile_phone = request.POST.get('mobile_phone')
#             code_name = request.POST.get('code_name')
#             code_num = request.POST.get('code_num')

#             marital_status = request.POST.get('marital_status')
#             #return HttpResponse(marital_status)
#            # marital_status = form.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=form.RadioSelect())
#             #return HttpResponse(marital_status )
#             birth_date = request.POST.get('birth_date')
            
#             if birth_date != "":
#                d = datetime.strptime(birth_date, '%d-%m-%Y')
#                birth_date = d.strftime('%Y-%m-%d')
#             else:
#                birth_date = None      
#             address = request.POST.get('address')
#             tags = request.POST.get('tags')
#             #return HttpResponse(address )
#             #return HttpResponse(birth_date )

#             date_of_exit = request.POST.get('date_of_joining')
#             if date_of_exit != "":
#                #return HttpResponse(date)
#                d = datetime.strptime(date_of_exit, '%d-%m-%Y')
#                date_of_exit = d.strftime('%Y-%m-%d')
#             else:
#                date_of_exit = None 
#             gender = request.POST.get('gender')
#             about_me = request.POST.get('about_me')
#             expertise = request.POST.get('expertise')
#             job_description = request.POST.get('job_description')

#             #created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             #updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             if not Employee.objects.filter(Q(employee_id=employee_id) | Q(email_id=email_id)).exists():
#                 obj = Employee.objects.create(employee_id=employee_id, first_name=first_name, 
#                 last_name=last_name, email_id=email_id, nick_name=nick_name,
#                 department=department,
#                 reporting_to=reporting_to,
#                 source_of_hire=source_of_hire,
#                 seating_location=seating_location,
#                 location=location,
#                 title=title,
#                 date_of_joining=date_of_joining,
#                 employee_status=employee_status,
#                 employee_type=employee_type,
#                 work_phone=work_phone,
#                 code_name=code_name,
#                 code_num=code_num,
#                 extension=extension,
#                 role=role,
#                 total_experience=total_experience, experience=experience,
                
#                 other_email=other_email, mobile_phone=mobile_phone,
#                 marital_status=marital_status, birth_date=birth_date,
#                 address=address, tags=tags,
                
#                 job_description=job_description, expertise=expertise,
#                 about_me=about_me, date_of_exit=date_of_exit, gender=gender,

#                 ) 
#                 obj.save()
#                 messages.success(request, first_name + ' Employee was created! ')
#                 html_template = loader.get_template( 'employee/index.html' )
#                 #return HttpResponse(html_template.render(request))
#                 #return render(request, "employees")
#                 return redirect('employees') 
#             else: 
#                 role = Group.objects.all()
#                 context_role = {
#                         'roles': role,
#                        }
          
#                 context_role.update({"form":form})  
#                 messages.error(request, ' Employee or EmailID Already Exists! ', context_role)
#                 context = {'form':form}
#                 return render(request, "employee/add_employee.html", context)
                
#             # if form.is_valid():
#             #     email_id = request.POST.get('email_id')
#             # else: 
#             #     messages.error(request, ' Employee Exists! ')
#             #     return render(request, "page-profile.html")
#             #added_by=added_by,
#             #added_time=added_time, 
#             #modified_by=modified_by,
#             # created_at=created_at, updated_at=updated_at,
#             #is_active=is_active)
            
#             #return HttpResponse('work')
#             # print(form.errors)
#             # print(role_name)
#             #g1 = Group.objects.create(name=role_name, role_type=role_type, description=description)
            
#             #html_template = loader.get_template( 'page-profile.html' )
#             #return HttpResponse(html_template.render(request))
#     # print(form.errors)
# #      context = {
# #         'all_cities': City.objects.all() 
# #     }
#     role = Group.objects.all()
#     context_role = {
#           'roles': role,
#          #  'country': 'in'
#        }
   
#     #
#    # tes = Group.objects.all()
#     context_role.update({"form":form})
#     print(context_role)
#     return render(request, "employee/add_employee.html",  context_role )
   
#    form = EmployeeForm(request.POST)
#    context = {} 
#      = {} 
#    if request.method == "POST":
#       #return HttpResponse(request.POST.get('input-employeeid'))
      
      
#       #context['form'] = form
#      # if request.POST:
# #       employee_id = request.POST.get('input-employeeid')
# #       context = {
    
# # }
# #       context['workers'] = employee_id #Employee.objects.all()
# #       context = {
# #     'employee_id': employee_id
# # }
      
    
#       if form.is_valid():
#                   return HttpResponse('working..')
#                   #temp = form.cleaned_data.get("geeks_field")
#                   #print(temp)
#                   return render(request, "page-profilesd.html")
#       else:
            
#             #return render(request, "page-profile.html" , {'form': form})
#             #return render('page-profiles.html', RequestContext(request, {
#              #     'employee_id':employee_id}))
#             #return render(request, 'page-profile.html', context )
#             html_template = loader.get_template( 'page-profile.html' )
#             #return render(request, "page-profile.html" , {'form': form})
#             form = EmployeeForm(None)
#             messages.success(request, 'error')
#             args = {'form': form} 
#             text = "hello world"
#            # form = EmployeeForm()
#            # args['mytext'] = text
#             return HttpResponse(html_template.render(args, request))
#    else:
#       return render(request, "page-profiless.profiles" , {'form': form})
#     messages.add_message(self.request, messages.INFO, 'Hello world.')
#     #super().form_valid(form)
#     return HttpResponseRedirect(self.get_success_url())
    
    

      #   form = EmployeeForm(request.POST) 
      #   obj = Employee.objects.create(employee_id=employee_id, first_name=first_name)
      #   obj.save() 
       
      #   if form.is_valid():  
      #       try:   
      #           form.save()  
      #           return redirect('/show')  
      #       except:  
      #           pass  
      #   else:  
      #   form = EmployeeForm()  
       
    #return render(request,'page-profile.html',{'form':form})
