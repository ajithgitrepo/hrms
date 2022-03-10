
from django.db import models
from django.contrib.auth.models import User 
from app.models.business_unit_model import Business_Unit 



# Create your models here.

class Variable_Salary(models.Model):  
   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank = False, null = False)
    businessunit = models.ForeignKey(Business_Unit, max_length=50, blank=True, related_name='businessunit', null=True, on_delete= models.SET_NULL)
  
    description = models.TextField(blank = False, null = False)  
    
    added_by = models.CharField(max_length=30,blank = True, null = True) 
    updated_by = models.CharField(max_length=30,blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    is_active = models.PositiveSmallIntegerField(default=1)
    device = models.CharField(max_length=20, blank = True, null = True)  

      
    class Meta:  
        db_table = "variable_salary"  

    def __str__(self):
        return self.name

 