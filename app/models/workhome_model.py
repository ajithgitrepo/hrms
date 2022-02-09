from django.db import models
from django.contrib.auth.models import User

from app.models.employee_model import Employee 


# Create your models here.

class Workhome(models.Model):  
   
    id = models.AutoField(primary_key=True)
    start_date = models.DateField(max_length=30,blank = False, null = False)
    end_date=models.DateField(max_length=30,blank = False, null = False)
    reason = models.TextField(blank = False, null = False)
    employee = models.ForeignKey(Employee, max_length=50, blank=True, related_name='employee', null=True, on_delete= models.SET_NULL)
    created_by = models.ForeignKey(Employee, blank=True, null=True, related_name='created_by', on_delete= models.SET_NULL)
    updated_by = models.ForeignKey(Employee, blank=True, null=True, related_name='updated_by', on_delete= models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    updated_at = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    is_approved = models.CharField(max_length=20, blank = True, null = True,default=0)  
    device = models.CharField(max_length=20, blank = True, null = True)  
   
      
    class Meta:  
        db_table = "work_from_home"  

 