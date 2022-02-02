from django import forms  
from app.models import Employee, Work_Experience, Education, Dependent

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

class EmployeeForm(forms.ModelForm):  
   
   # marital_status = forms.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=forms.RadioSelect())

    class Meta:  
        model = Employee  
       # fields = "__all__",   "mobile_number",
        fields =("employee_id", "first_name", "last_name",  "email_id") #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active', 'code_num']



