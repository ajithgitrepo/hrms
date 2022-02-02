from django import forms  
from app.models import Exit_Employee_Detail

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

from django.conf import settings

from django.forms import ModelForm, Textarea

class Exit_EmployeeForm(forms.ModelForm):  
   
   # marital_status = forms.ChoiceField(choices=Employee.MARITAL_CHOICES, widget=forms.RadioSelect())
   # seperation_date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:  
        model = Exit_Employee_Detail  
       # fields = "__all__",   "mobile_number", 
        reason_leaving = forms.CharField(widget=forms.Textarea)
       
        fields = [ "employee", "seperation_date",  "reason_leaving", ] #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active']
        widgets = { 
            'reason_leaving': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

    def __init__(self, *args, **kwargs):
      super(Exit_EmployeeForm, self).__init__(*args, **kwargs)

      self.fields['employee'].required = True
      self.fields['employee'].widget.attrs['required'] = 'required'
      self.fields['employee'].error_messages = {'required': 'Employee is required'} 

      self.fields['reason_leaving'].required = True
      self.fields['reason_leaving'].widget.attrs['required'] = 'required'
      self.fields['reason_leaving'].error_messages = {'required': 'Reason for leaving is required'} 

      self.fields['seperation_date'].required = True
      self.fields['seperation_date'].widget.attrs['required'] = 'required'
      self.fields['seperation_date'].error_messages = {'required': 'Seperation Date is required'} 

      self.fields[ 'seperation_date' ].input_formats = [ '%d-%m-%Y' ]    



