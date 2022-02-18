from django import forms  
from app.models import Employee
# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError  

class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'role_type']
        # widgets = {
        #     'permissions': FilteredSelectMultiple("Permission", False, attrs={'rows':'2'}),
        # }
        # widgets={
        #            "name":forms.TextInput(attrs={'placeholder':'Role Name','name':'name','id':'name_id','class':'form-control'}),
        #         }
    def clean_name(self):
        role_name = self.cleaned_data['name']
        qs = Group.objects.filter(name=role_name)
        if self.instance.pk is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("There is already a role with name: %s" % role_name)
        # if Group.objects.filter(name=role_name).exists():
        #     raise ValidationError("Role name already exists")
        return role_name