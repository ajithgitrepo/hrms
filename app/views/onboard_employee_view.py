

from app.models import onboard_employee_model
from app.models.onboard_employee_model import Onboard_Employee, Onboard_Work_Experience, Onboard_Education
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.Onboard_EmployeeForm import Onboard_EmployeeForm
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa  
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.conf import settings as django_settings
import os
from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
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
from django.utils import timezone
import os
from django.core.files.storage import FileSystemStorage

from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
import random
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

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

def snippets_candidate_all_info(request):
    roles = Group.objects.filter(is_active='1')
    emp_id =    request.POST.get('emp_id')
    csrf =    request.POST.get('csrfmiddlewaretoken')
    #final_list = Onboard_Employee.objects.filter(candidate_id  = emp_id)
    final_list = Onboard_Employee.objects.filter(candidate_id  = emp_id).annotate(test=Subquery(Group.objects.filter(id = OuterRef('title')).values('role_type')))
    #print(final_list)
    #return HttpResponse(final_list)
    test = final_list.values_list('title', flat=True)

    jsondata = serializers.serialize('json', final_list)
 
    return HttpResponse(jsondata, content_type='application/json')
 

def onboard_employees(request):
   # return HttpResponse("employee")
    employee = Onboard_Employee.objects.filter(is_active='1')
   # return HttpResponse(employee)
    # print(employee)
    context = {'employees':employee}
    return render(request, "onboard_employee/index.html", context)

def add_onboard_employee(request):  
   # return render(request, "onboard_employee/add_onboard_employee.html")
    form = Onboard_EmployeeForm()
    #return HttpResponse(request.method)
   # """
    if request.method == 'POST':
        form = Onboard_EmployeeForm(request.POST)
        if form.is_valid():
           
            """
            fss = FileSystemStorage()
            file_name = fss.save(upload.name, upload)
            file_url = fss.url(file_name)
            """
            Photo_name = ""
            upload = request.FILES['upload']
            if upload != None: 
                logoRoot = os.path.join(settings.MEDIA_ROOT, 'profile_images/')
            
                #logo_url = os.path.join(settings.MEDIA_URL, 'profile_images/')
                logoRoot=logoRoot.replace("\\","/")
                Photo_name = upload.name
               # return HttpResponse(upload.name) 
                fs = FileSystemStorage(location=logoRoot)
                file_name = fs.save(upload.name, upload)
                file_url = fs.url(file_name)

            number = random.randint(1000, 9999)
            res = str('CAD') + str(number)
           
            email_id = request.POST.get('email_id')
            #return HttpResponse(email_id)
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            mobile_number = request.POST.get('mobile_number')
            #nick_name = request.POST.get('nick_name')
            official_email_id = request.POST.get('official_email')
            
            #mobile_phone = request.POST.get('mobile_phone')
            code_name = request.POST.get('code_name')
            code_num = request.POST.get('code_num')
           
            emirate_id = request.POST.get('emirate_id')

            address = request.POST.get('address')
            
            state = request.POST.get('state')
            city = request.POST.get('city')
            pin_code = request.POST.get('pin_code')
            country = request.POST.get('country')
            experience = request.POST.get('experience')
            
            source_of_hire = request.POST.get('source_of_hire')

            skill_set = request.POST.get('skill_set')
             
            highest_qualify = request.POST.get('highest_qualify')
            additional_info = request.POST.get('additional_info')
            current_sal = request.POST.get('current_sal')

            offer_letter_url = request.POST.get('offer_letter_url')


            tentative_joining_date = request.POST.get('tentative_joining_date')
            if tentative_joining_date != "":
               #return HttpResponse(date)   
               d = datetime.datetime.strptime(tentative_joining_date, '%d-%m-%Y')
               tentative_joining_date = d.strftime('%Y-%m-%d')
            else:
               tentative_joining_date = None    
            
            #return HttpResponse(role)
            location = request.POST.get('location')
            title = request.POST.get('title')

            created_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            updated_at =  timezone.now()#.strftime('%Y-%m-%d %H:%M:%S')
            is_active = '1'
            if not Onboard_Employee.objects.filter( Q(email_id=email_id)).exists():
                obj = Onboard_Employee.objects.create( 
                candidate_id = res,
                first_name=first_name, 
                last_name=last_name, email_id=email_id, 
                mobile_number=mobile_number,
                code_name=code_name,
                code_num=code_num,
                official_email_id=official_email_id,
                photo_url=Photo_name, 
                emirate_id=emirate_id,
                address=address,
                state=state,
                city=city,
                pin_code=pin_code,
               
                country=country,
                experience=experience,
                source_of_hire=source_of_hire,
               
                skill_set=skill_set,
                highest_qualify=highest_qualify,
                additional_info=additional_info, current_sal=current_sal,
                
                offer_letter_url=offer_letter_url, tentative_joining_date=tentative_joining_date,
                location=location, title=title,
                
                created_at=created_at, updated_at=updated_at, is_active=is_active,

                ) 
                obj.save()
    
                latest_id = Onboard_Employee.objects.latest('candidate_id').candidate_id
               # return HttpResponse(latest_id)
                
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
                        d = datetime.datetime.strptime(from_date[i], "%d-%m-%Y")
                        d2 = datetime.datetime.strptime(to_date[i], "%d-%m-%Y")
                       # return HttpResponse(latest_id)
                        exp = Onboard_Work_Experience.objects.create(previous_company_name=previous_company_name[i], job_title=job_title[i], from_date= d.strftime('%Y-%m-%d'), to_date=d2.strftime('%Y-%m-%d'), job_description=job_description[i], candidate_id = latest_id )
                     
                c = min([len(school_name), len(degree), len(field), len(date_of_completion), len(interests)])
                
                for i in range(c):
                    if school_name[i] and degree[i] and field[i] and date_of_completion[i] and interests[i] :
                        d = datetime.datetime.strptime(date_of_completion[i], "%d-%m-%Y")
                        edu = Onboard_Education.objects.create(school_name=school_name[i], degree=degree[i], date_of_completion= d.strftime('%Y-%m-%d'), field=field[i], interests=interests[i], candidate_id = latest_id )
                      
                c = min([len(dependent_name), len(relationship), len(date_of_birth)])
        
                return redirect('onboard_employees') 
            else: 
                role = Group.objects.all()
                context_role = {
                        'roles': role,
                       }
          
                context_role.update({"form":form})  
                messages.error(request, ' Employee or EmailID Already Exists! ', context_role)
                context = {'form':form}
                return render(request, "onboard_employee/add_onboard_employee.html", context)
       

    role = Group.objects.all()
    context_role = {
          'roles': role,
         #  'country': 'in'
       }
   
  
   # tes = Group.objects.all()
    context_role.update({"form":form})
    # print(context_role)
    return render(request, "onboard_employee/add_onboard_employee.html",  context_role )
   

def delete_onboard_employee(request, pk):
   # return HttpResponse('working..')
    data = Onboard_Employee.objects.get(candidate_id =pk)
    data.is_active = 0
    data.save()
    messages.success(request, 'Employee was deleted! ')
    return redirect('onboard_employees')

def send_offer_letter(request):
    
    my_host = 'smtp.gmail.com'
    my_port = 587
    my_username = 'ajithrockers007@gmail.com'
    my_password = 'GmailPassword7'
    my_use_tls = True

    connection = get_connection(host=my_host, 
        port=my_port, 
        username=my_username, 
        password=my_password, 
        use_tls=my_use_tls
    ) 

    # send_mail('diditwork?', 'test message', 'from_email', ['to'], connection=connection)

    details = Onboard_Employee.objects.filter(candidate_id=request.GET.get('can_id'))
    # print(details[0].first_name)

    myDate = datetime.datetime.now()
    context_dict={'fname': details[0].first_name,'lname': details[0].last_name, 'nationality': request.GET.get('can_nation'), 'mobile': request.GET.get('can_mobile'), 'joining_date': request.GET.get('can_joindate'), 'accept_date': request.GET.get('can_acceptdate'), 'salary': request.GET.get('can_salary'), 'position': request.GET.get('can_position'), 'email': details[0].email_id, 'aadhar': request.GET.get('can_aadhar'), 'hr_name': request.user.first_name }
    template = get_template('mail_templates/appoinment.html')
    html  = template.render(context_dict)
    result = BytesIO()

    myDate = datetime.datetime.now()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        # return HttpResponse(result.getvalue(), content_type='application/pdf')
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = "offer_letter"+'-'+details[0].first_name+" "+details[0].last_name+"-"+myDate.strftime("%d-%m-%Y")+".pdf"
        content = "inline; filename=%s" %(filename)

        file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'offer_letters')

        with open(os.path.join(file_upload_dir, filename), 'wb+') as output:
            appoinment_letter = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)

            update = Onboard_Employee.objects.filter(candidate_id=request.GET.get('can_id')).update(
                offer_letter_url = filename,
            )

            subject = 'Welcome to TTF world'
            html_message = render_to_string('mail_templates/candidate_greetings.html', {'fname': details[0].first_name, 'lname': details[0].last_name, 'hr_name': request.user.first_name})
            plain_message = strip_tags(html_message)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [details[0].email_id]
        
            email = EmailMultiAlternatives(
                subject,
                plain_message,
                email_from,
                recipient_list,
            )

            email.attach_alternative(html_message, 'text/html')
            email.attach('offer_letter.pdf', result.getvalue() , 'application/pdf')
            email.send()
    
        # Download the file
        # download = request.GET.get("download")
        # if download:
        #     content = "attachment; filename=%s" %(filename)

        # response['Content-Disposition'] = content
        # return response

        return HttpResponse(1)

 
    return HttpResponse(0)


def preview_offer_letter(request):
   
    details = Onboard_Employee.objects.filter(candidate_id=request.GET.get('can_id'))
    # print(details[0].first_name)

    myDate = datetime.datetime.now()
    context_dict={'fname': details[0].first_name,'lname': details[0].last_name, 'nationality': request.GET.get('can_nation'), 'mobile': request.GET.get('can_mobile'), 'joining_date': request.GET.get('can_joindate'), 'accept_date': request.GET.get('can_acceptdate'), 'salary': request.GET.get('can_salary'), 'position': request.GET.get('can_position'), 'email': details[0].email_id, 'aadhar': request.GET.get('can_aadhar'), 'hr_name': request.user.first_name }
    template = get_template('mail_templates/appoinment.html')
    html  = template.render(context_dict)
    result = BytesIO()

    myDate = datetime.datetime.now()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        # return HttpResponse(result.getvalue(), content_type='application/pdf')
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = "offer_letter"+'-'+details[0].first_name+" "+details[0].last_name+"-"+myDate.strftime("%d-%m-%Y")+".pdf"
        content = "inline; filename=%s" %(filename)

        file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'offer_letters')

        with open(os.path.join(file_upload_dir, filename), 'wb+') as output:
            appoinment_letter = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)

        return HttpResponse(filename)

    return HttpResponse(0)


def convert_to_emp(request, pk):

    candidate = Onboard_Employee.objects.filter(candidate_id = pk)
    
    education = Onboard_Education.objects.filter(candidate_id = pk)

    experience = Onboard_Work_Experience.objects.filter(candidate_id = pk)
    # print(experience)

    number = random.randint(1000, 9999)
    employee_id = str('Emp') + str(number)
    
    if not Employee.objects.filter(Q(email_id=candidate[0].email_id)).exists():
        obj = Employee.objects.create(
            employee_id=employee_id, 
            first_name=candidate[0].first_name, 
            last_name=candidate[0].last_name, 
            email_id=candidate[0].email_id, 
            nick_name='emp',
            department_id=1, 
            role_id=1,
            mobile_phone=candidate[0].mobile_number,
        
        ) 
        obj.save()

        latest_id = employee_id

        hashed_pwd = make_password("secret")

        obj = User(
            password=hashed_pwd,
            is_superuser=1, 
            first_name=candidate[0].first_name, 
            last_name=candidate[0].last_name, 
            email=candidate[0].email_id,
            role=1,
            emp_id=latest_id,
            is_staff=1,
            is_active=1,
            date_joined=datetime.datetime.now(),
            
        ) 

        obj.save()

        for edu in education:
            edu = Education.objects.create(school_name=edu.school_name, degree=edu.degree, date_of_completion= edu.date_of_completion, field=edu.field, interests=edu.interests, employee_id= employee_id )

        for exe in experience:
            exp = Work_Experience.objects.create(previous_company_name=exe.previous_company_name, job_title=exe.job_title, from_date= exe.from_date, to_date=exe.to_date, job_description=exe.job_description, employee_id= employee_id )

        update = Onboard_Employee.objects.filter(candidate_id=pk).update(
            is_active = 0,
        )

        messages.success(request, ' Candidate Converted as Employee! ')
   
    else: 
        messages.error(request, ' Employee or Email-ID Already Exists! ')

    return redirect('onboard_employees')