
from django.db import models
from django.contrib.auth.models import User 
from app.models.department_model import Department 



# Create your models here.

class Business_Unit(models.Model):  
   
    id = models.AutoField(primary_key=True)
    business_unit = models.CharField(max_length=100, blank = False, null = False)
    company = models.ForeignKey(Department, max_length=50, blank=True, related_name='department', null=True, on_delete= models.SET_NULL)
  
    description = models.CharField(max_length=300, blank = False, null = False)  
    
    added_by = models.CharField(max_length=30,blank = True, null = True) 
    updated_by = models.CharField(max_length=30,blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  

      
    class Meta:  
        db_table = "business_unit"  

    def __str__(self):
        return self.name

 