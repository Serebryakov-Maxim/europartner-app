from .models import mw_Detail
from django.forms import ModelForm, TextInput, DateInput, Select, RadioSelect, SelectDateWidget, CheckboxInput, NumberInput

class DetailForm(ModelForm):
    class Meta:
        model = mw_Detail
        fields = ['name', 'full_name', 'article', 'assembly', 'shield', 'type', 'quantity', 'partner', 'date_start', 'date_finish', 'status']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наименование',
                'id': 'inputName',
            }),
            "full_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Полное наименование',
                'id': 'inputFullName',
            }),

            "assembly": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сборка',
                'id': 'inputAssembly',
            }),
            "type": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Тип',
                'id': 'inputType',
            }),
            "quantity": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество, шт.',
                'id': 'inputQuantity',
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
            "partner": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Клиент',
                'id': 'inputPartner',
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
            "status": Select(attrs={
                'class': 'form-select',
                'placeholder': 'Статус',
                'id': 'inputStatus',
            }),
        }