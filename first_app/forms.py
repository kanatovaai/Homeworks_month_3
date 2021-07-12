from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import TextInput, NumberInput, Select

from .models import Product, Review


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'title description price category'.split()
        widgets = {
            'title': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите имя продукта'
                }
            ),
            'description': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите опиание продукта'
                }
            ),
            'price': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите цену продукта'
                }
            ),
            'category': Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = 'text product'.split()
        widgets = {
            'text': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите отзыв'
                }
            ),
            'product': Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }


class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Пароль',
                                          'class': 'form-control'}
                               ))
    password1 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Повторите пароль',
                                           'class': 'form-control'}
                                ))

    def clean_email(self):
        users = User.objects.filter(username=self.cleaned_data['email'])
        if users.count() > 0:
            raise ValidationError('сущ!')


