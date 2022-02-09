from django import forms  
from app.models import Workhome

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

class WorkhomeForm(forms.ModelForm):  
   
   # marital_status = forms.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=forms.RadioSelect())

    class Meta:  
        model = Workhome  
       # fields = "__all__",   "mobile_number",
        fields =('reason','start_date','end_date',) 
        readonly_fields = ['created_at', 'updated_at', 'is_active']



