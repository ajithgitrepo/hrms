from django import forms  
from app.models import Project

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

class ProjectForm(forms.ModelForm):  
  
    class Meta:  
        model = Project  
       # fields = "__all__",   "mobile_number",
        fields =('project_name','project_client','project_manager','project_users') 
        readonly_fields = ['created_at', 'updated_at', 'is_active']



