from django import forms  
from app.models import Organization_Files

from django.core.exceptions import ValidationError  

class Organization_Files_Form(forms.ModelForm):  
   
    class Meta:  
        model = Organization_Files  
        fields =("file","name") 

