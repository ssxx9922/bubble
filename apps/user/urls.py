#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/3/26 PM2:52'

from user.views import loginView, registerView, activeView, resetView, forgetPwdView
from django.urls import path


urlpatterns = [
    path('login', loginView.as_view()),
    path('register', registerView.as_view()),
    path('active/<str:active_code>/', activeView.as_view()),
    path('forgetPwd', forgetPwdView.as_view()),
    path('reset/<str:active_code>/', resetView.as_view()),

]