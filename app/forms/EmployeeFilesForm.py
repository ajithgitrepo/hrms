from django import forms  
from app.models import Employee_Files

from django.core.exceptions import ValidationError  

class Employee_Files_Form(forms.ModelForm):  
   
    class Meta:  
        model = Employee_Files  
        fields =("file",) 

