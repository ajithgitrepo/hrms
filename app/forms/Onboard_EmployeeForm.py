from django import forms  
from app.models import Onboard_Employee, Work_Experience, Education

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

class Onboard_EmployeeForm(forms.ModelForm):  
   
   # marital_status = forms.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=forms.RadioSelect())

    class Meta:  
        model = Onboard_Employee  
       # fields = "__all__",   "mobile_number",
        fields =("first_name", "last_name",  "email_id", "mobile_number","emirate_id", "country")
        readonly_fields = ['created', 'updated_at', 'is_active', 'code_num']



