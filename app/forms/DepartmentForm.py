from django import forms  
from app.models.department_model import Department

from django.core.exceptions import ValidationError  

class DepartmentForm(forms.ModelForm):  
   
    class Meta:  
        model = Department  
       # fields = "__all__",   "mobile_number",
        fields = [ "name" ] #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active']
      

        


   


