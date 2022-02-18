<<<<<<< HEAD
from django import forms  
from app.models.reporting_to_model import Reporting

from django.core.exceptions import ValidationError  

class ReportForm(forms.ModelForm):  
   
    class Meta:  
        model = Reporting   
       # fields = "__all__",   
        fields = [ "employee", "reporting", ] 
        readonly_fields = ['created', 'updated_at', 'is_active']

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        
        self.fields['employee'].required = True
        self.fields['employee'].widget.attrs['required'] = 'required'
        self.fields['employee'].error_messages = {'required': 'Employee is required'}

        self.fields['reporting'].required = True
        self.fields['reporting'].widget.attrs['required'] = 'required'
        self.fields['reporting'].error_messages = {'required': 'Reporting To is required'}
          
      

        


   


=======
from django import forms  
from app.models.reporting_to_model import Reporting

from django.core.exceptions import ValidationError  

class ReportForm(forms.ModelForm):  
   
    class Meta:  
        model = Reporting   
       # fields = "__all__",   
        fields = [ "employee", "reporting", ] 
        readonly_fields = ['created', 'updated_at', 'is_active']

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        
        self.fields['employee'].required = True
        self.fields['employee'].widget.attrs['required'] = 'required'
        self.fields['employee'].error_messages = {'required': 'Employee is required'}

        self.fields['reporting'].required = True
        self.fields['reporting'].widget.attrs['required'] = 'required'
        self.fields['reporting'].error_messages = {'required': 'Reporting To is required'}
          
      

        


   


>>>>>>> origin/hrms-09-02-2022
