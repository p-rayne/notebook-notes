import datetime

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from .models import CustomUser, Notes
from .widget import DatePickerInput


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2


class NotesForm(forms.ModelForm):
    text = forms.CharField(label='Текст заметки', widget=forms.Textarea(attrs={'class': 'form-input'}))
    category = forms.CharField(label='Категория', widget=forms.TextInput(attrs={'class': 'form-input',
                                                                                'value': 'Без категории',
                                                                                'placeholder': 'Введите категорию'}))

    class Meta:
        model = Notes
        fields = ('text', 'category')


class SearchForm(forms.Form):
    datemin = forms.DateField(widget=DatePickerInput(attrs={
        'class': 'form-control search_field', 'min': '2022-01-01', 'max': datetime.date.today(),
        'value': "2022-01-01"
    }), label='Начальная дата')
    datemax = forms.DateField(widget=DatePickerInput(attrs={
        'class': 'form-control search_field', 'min': '2022-01-01', 'max': datetime.date.today(),
        'value': datetime.date.today()
    }), label='Финальная дата')
    text_search = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control search_field', 'placeholder': 'Поиск...', 'aria-label': 'Search'
    }), label='Поиск по словам', required=False)
    cat_search = forms.ModelChoiceField(queryset=Notes.objects.none(), widget=forms.Select(attrs={
        'class': "form-select search_field", 'aria-label': "Default select example",
    }), required=False, label='Поиск по категориям')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['cat_search'].queryset = Notes.objects.filter(author=self.user). \
            values_list('category', flat=True).distinct('category')
