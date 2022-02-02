
from django.utils.functional import partition
from app.models.employee_files_model import Employee_Files
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import context, loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
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
from app.models.employee_model import Employee
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
from app.forms.EmployeeFilesForm import Employee_Files_Form
from app.models.folder_model import Folder
from django.views import generic
from django.db.models import Avg, Count, Min, Sum

# def index(request): 
#     org_files = Organization_Files.objects.filter(is_active = 1)
#     context = {
#         'org_files' : org_files,
#     }
#     return render(request, "organization_files/index.html",  context )

class IndexView(generic.ListView):

    model = Employee_Files
    template_name = "employee_files/index.html"
    # context_object_name = 'emp_files'

    # Return without any functions
    # queryset = Employee_Files.objects.filter(is_active = 1, employee__is_active = 1)

    # Using get_queryset
    def get_queryset(self) :
        queryset = Employee_Files.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['emp_files'] = Employee_Files.objects.filter(is_active = 1, employee__is_active = 1)
        context['folders'] = (Employee_Files.objects.filter(is_active = 1).values('folder').annotate(dcount=Count('folder')).order_by('folder'))
    
        return context

    

def add_folder(request): 

    if not Folder.objects.filter( Q(name = request.GET.get('folder_name'))).exists():
        obj = Folder.objects.create( 
            name = request.GET.get('folder_name'),
            device = 'web',
            added_by_id= request.user.emp_id,
            updated_by_id= request.user.emp_id,
            
        )   
        return HttpResponse(1)
    else:
        return HttpResponse(0)
        


def add_emp_files(request):  

    form = Employee_Files_Form(request.POST, request.FILES or None)

    if request.method == 'POST':
        form = Employee_Files_Form(request.POST, request.FILES)

        if form.is_valid():

            files = request.FILES.getlist("file")
            current_date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            extension = ""
            file_name = ""
            
            for f in files:
             #name1 = os.path.splitext(str(f.name))[1]  request.POST.get('name')
              file_name, extension = os.path.splitext(f.name) 
              handle_uploaded_file(f, file_name, request.POST.get('folder'), current_date_time)  
            
              if request.POST.get('date_until'):
                date = datetime.datetime.strptime(request.POST.get('date_until'), "%d-%m-%Y")
                db_date = date.strftime('%Y-%m-%d')
              else:
                db_date = None

              obj = Employee_Files.objects.create( 
                file = file_name+"-"+current_date_time+""+extension,
                name = file_name,     
                description = request.POST.get('description'),
                device = 'web',
                employee_id= request.POST.get('employee'),
                added_by_id= request.user.emp_id,
                updated_by_id= request.user.emp_id,
                valid_until= db_date, 
                folder = request.POST.get('folder'),
               )

            return redirect('employee_files') 

    folders = Folder.objects.filter(is_active = 1)
    employees = Employee.objects.filter(is_active = 1)
    # print(employees)

    context = {
        'form' : form,
        'folders' : folders,
        'employees' : employees,
    }

    return render(request, "employee_files/add_emp_files.html",  context )


  #return HttpResponse(file_name)


            # if request.FILES.getlist('file', False):
            #     name = os.path.splitext(str(request.FILES['file']))[0]
            #     extesion = os.path.splitext(str(request.FILES['file']))[1]
            #    # handle_uploaded_file(request.FILES['profile'], current_date_time, 'profile_images')
            #     file_name = name   #+"-"+current_date_time+""+extesion
            # else:
            #     file_name = None
            
      # for i in range(0, len(request.FILES))]
      #       #return HttpResponse(files) 
      #       current_date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  
      #       handle_uploaded_file(request.FILES['file'], request.POST.get('name'), request.POST.get('folder'), current_date_time)
      #       extesion = os.path.splitext(str(request.FILES['file']))[1]
            

def handle_uploaded_file(f, name, folder, current_date_time):
    
    extesion = os.path.splitext(str(f))[1]
    file_name = name+"-"+current_date_time+""+extesion
    if folder !=None:
        directory = folder
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'files/employee/'+directory), exist_ok=True)
        file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'files/employee/'+directory)

    else:
        file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'files/employee')

    with open(os.path.join(file_upload_dir, file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def delete_emp_file(request, pk):
   # return HttpResponse('working..')
    data = Employee_Files.objects.get(id = pk)
    data.is_active = 0
    data.save()
    messages.success(request, 'File was deleted! ')
    # return redirect('employee_files')

    return redirect(request.META.get('HTTP_REFERER'))