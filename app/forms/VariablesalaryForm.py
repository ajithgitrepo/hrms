from django import forms  
from app.models.variable_salary_model import Variable_Salary

from django.core.exceptions import ValidationError  

class VariablesalaryForm(forms.ModelForm):  
   
    class Meta:  
        model = Variable_Salary  
       # fields = "__all__",   "mobile_number",
        fields = [ "name" ] #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active']
      

        


   


