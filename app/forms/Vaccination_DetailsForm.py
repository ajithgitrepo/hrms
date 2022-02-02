from django import forms  
from app.models import Vaccination_Detail

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

from django.conf import settings

from django.forms import ModelForm, Textarea

class Vaccination_DetailForm(forms.ModelForm):  
   

    class Meta:  
        model = Vaccination_Detail  
       # fields = "__all__",   "mobile_number", 
     
        fields = [ "vaccinated_status", ] #"role", "department") #"date_of_joining")
        readonly_fields = ['created', 'updated_at', 'is_active']
      
        
    def __init__(self, *args, **kwargs):
      super(Vaccination_DetailForm, self).__init__(*args, **kwargs)
      
      # self.fields['employee'].required = True 
      # self.fields['employee'].widget.attrs['required'] = 'required'
      # self.fields['employee'].error_messages = {'required': 'Employee is required'} 

      self.fields['vaccinated_status'].required = True
      self.fields['vaccinated_status'].widget.attrs['required'] = 'required'
      self.fields['vaccinated_status'].error_messages = {'required': 'vaccinated_status is required'} 

      # self.fields['given_date'].required = True
      # self.fields['given_date'].widget.attrs['required'] = 'required'
      # self.fields['given_date'].error_messages = {'required': 'Given Date is required'} 

      # self.fields[ 'partial_vacci_date' ].input_formats = [ '%d-%m-%Y' ]    
      # self.fields[ 'date_of_vaccination' ].input_formats = [ '%d-%m-%Y' ]   



