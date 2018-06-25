#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/3/26 PM2:52'

from rest_framework_jwt.views import obtain_jwt_token

from user.views import registerEmailView, activeView, resetView, forgetPwdView, changePwdView, registerEmailCodeViewset
from django.urls import path


urlpatterns = [
    path('login', obtain_jwt_token),
    path('registerEmail', registerEmailCodeViewset),
    path('active/<str:active_code>/', activeView.as_view()),
    path('forgetPwd', forgetPwdView.as_view()),
    path('reset/<str:active_code>/', resetView.as_view()),
    path('changePwd',changePwdView.as_view())
]