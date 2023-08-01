from .models import Pressform
from django.forms import ModelForm, TextInput, DateInput, Select, RadioSelect, SelectDateWidget, CheckboxInput

class PressformForm(ModelForm):
    class Meta:
        model = Pressform
        fields = ['name', 'article', 'assembly', 'shield', 'date_start', 'date_finish', 'type', 'status']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наименование',
                'id': 'inputName',
            }),
            "assembly": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сборка',
                'id': 'inputAssembly',
            }),
            "shield": CheckboxInput(attrs={
                'class': 'form-check form-check-input',
                'type': 'checkbox',
                'placeholder': 'Шильда',
                'id': 'inputShield',
            }),
            "article": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Артикул',
                'id': 'inputArticle',
            }),
            "date_start": TextInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'inputDateStart',
            }),
            "date_finish": TextInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'inputDateFinish',
            }),
            "type": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Тип',
                'id': 'inputType',
            }),
            "status": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Статус',
                'id': 'inputStatus',
            }),
        }