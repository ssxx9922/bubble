#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/3/27 AM10:22'

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=6, max_length=30)
    password = forms.CharField(required=True, min_length=6, max_length=20)

class RegisterForm(forms.Form):
    username = forms.EmailField(required=True, min_length=6, max_length=30)
    password = forms.CharField(required=True, min_length=6, max_length=20)

class FergetPwdForm(forms.Form):
    username = forms.EmailField(required=True, min_length=6, max_length=30)

class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)
