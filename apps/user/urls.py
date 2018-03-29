#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/3/26 PM2:52'

from user.views import loginView, registerEmailView, activeView, resetView, forgetPwdView, changePwdView
from django.urls import path


urlpatterns = [
    path('login', loginView.as_view()),
    path('registerEmail', registerEmailView.as_view()),
    path('active/<str:active_code>/', activeView.as_view()),
    path('forgetPwd', forgetPwdView.as_view()),
    path('reset/<str:active_code>/', resetView.as_view()),
    path('changePwd',changePwdView.as_view())
]