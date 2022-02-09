from django.db import models
from django.contrib.auth.models import User 
from app.models.client_model import *
from app.models.employee_model import *
from app.models.department_model import *

# Create your models here.

class Project(models.Model):  
   
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100 , blank = False, null = False)
    project_client = models.ForeignKey(Client, max_length=50, blank=False, related_name='project_client', null=True, on_delete= models.SET_NULL)
    project_head = models.ForeignKey(Employee, blank=False, null=True, related_name='project_head', on_delete= models.SET_NULL)
    project_manager = models.ForeignKey(Employee, blank=False, null=True, related_name='project_manager', on_delete= models.SET_NULL)
    project_users= models.CharField(max_length=255 , blank = False, null = True)
    project_cost = models.CharField(max_length=30 , blank = False, null = False)
    project_description = models.CharField(max_length=30 , blank = False, null = False)

    created_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  
   
      
    class Meta:  
        db_table = "project"  

 