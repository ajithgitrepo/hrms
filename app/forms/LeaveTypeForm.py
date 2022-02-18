<<<<<<< HEAD
from django import forms  
from app.models import Employee, Work_Experience, Education, Dependent, Leave_Type

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError

class LeaveTypeForm(forms.ModelForm):  
   
    # units = (
    #     (1,'Day'),
    #     (0,'Hours')
    # )


    # unit = forms.ChoiceField(required = True, choices = units, widget=forms.RadioSelect(attrs={'class' : 'custom-control-input'}), initial=1)

    # unit = forms.ChoiceField(choices=units, widget=forms.RadioSelect(attrs={'class': ''}))

    class Meta:  
        model = Leave_Type  

        fields =("name", "type")
        readonly_fields = ['created_at', 'updated_at', 'is_active','description']

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Leave_Type.objects.filter(name=name)
        if self.instance.pk is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("There is already a leave type with name: %s" % name)
        # if Group.objects.filter(name=role_name).exists():
        #     raise ValidationError("Role name already exists")
        return name



=======
from django import forms  
from app.models import Employee, Work_Experience, Education, Dependent, Leave_Type

# from app.models import Group
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError

class LeaveTypeForm(forms.ModelForm):  
   
    # units = (
    #     (1,'Day'),
    #     (0,'Hours')
    # )


    # unit = forms.ChoiceField(required = True, choices = units, widget=forms.RadioSelect(attrs={'class' : 'custom-control-input'}), initial=1)

    # unit = forms.ChoiceField(choices=units, widget=forms.RadioSelect(attrs={'class': ''}))

    class Meta:  
        model = Leave_Type  

        fields =("name", "type")
        readonly_fields = ['created_at', 'updated_at', 'is_active','description']

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Leave_Type.objects.filter(name=name)
        if self.instance.pk is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("There is already a leave type with name: %s" % name)
        # if Group.objects.filter(name=role_name).exists():
        #     raise ValidationError("Role name already exists")
        return name



>>>>>>> origin/hrms-09-02-2022
