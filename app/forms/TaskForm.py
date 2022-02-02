from django import forms
from core import settings
from app.models.task_model import Task

from django.core.exceptions import ValidationError

class TaskForm(forms.ModelForm):
    start_date =forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    end_date =forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    reminder =forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        ordering = ['-id']
        paginate_by = 5
        model = Task
#         fields = ("__all__")
        fields = ("employee", 'task_name', 'start_date', 'end_date', 'priority')
        readonly_fields = ['created_at', 'updated_at', 'is_active']


        


   


