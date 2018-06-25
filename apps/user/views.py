
# Create your views here.
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework import status
# 登录
from rest_framework.response import Response

from apiData.result import Result
from user.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email
from user.serializers import CodeSerializer

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class registerEmailCodeViewset(CreateModelMixin,viewsets.GenericViewSet):
    """
    发送验证邮件
    """
    serializer_class = CodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validate_email['username']
        user_profile = UserProfile.objects.create_user(email, email, pass_word)
        user_profile.is_active = False
        user_profile.save()
        send_register_email(email=email, send_type='register')

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """



# 注册
class registerEmailView(View):
    def post(self, request):
        user_name = request.POST.get('username')
        users = UserProfile.objects.filter(email=user_name)
        if users.filter(is_active=True):
            return Result.error(message='该账号已经注册')
        if users.filter(is_active=False):
            if EmailVerifyRecord.objects.filter(email=user_name,
                                                send_type='register',
                                                is_valid=0,
                                                send_time__gte=datetime.now()-timedelta(minutes=30)):
                return Result.error(message='请查阅你邮箱中的激活邮件')
            else:
                send_register_email(email=user_name, send_type='register')
                return Result.error(message='该账号已注册,一封新的激活邮件已经发到您的邮箱,请尽快激活!')
        pass_word = request.POST.get('password')
        user_profile = UserProfile.objects.create_user(user_name, user_name, pass_word)
        user_profile.is_active = False
        user_profile.save()

        send_register_email(email=user_name, send_type='register')

        return Result.success()

# 激活邮箱
class activeView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code,
                                                       is_valid=0,
                                                       send_time__gte=datetime.now()-timedelta(minutes=30))
        if all_records:
            for record in all_records:
                #已使用状态置为1
                record.is_valid=1
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                record.save()
                # 激活成功重定向到此地址
                return HttpResponseRedirect('/registerSuccess')
        else:
            return Result.error('链接错误')

# 忘记密码
class forgetPwdView(View):
    def post(self,request):
        email = request.POST.get('email')
        if EmailVerifyRecord.objects.filter(email=email,
                                            send_type='forget',
                                            is_valid=0,
                                            send_time__gte=datetime.now() - timedelta(minutes=30)):
            return Result.error(message='发送邮件过于频繁')
        if UserProfile.objects.filter(email=email,is_active=True):
            send_register_email(email, 'forget')
            return Result.success()
        else:
            return Result.error('邮箱输入错误')

#重置密码
class resetView(View):
    def get(self,request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code,send_type='forget',is_valid=0,send_time__gte=datetime.now()-timedelta(minutes=30))
        if all_records:
            if len(all_records) > 0:
                return render(request, 'resetPwd.html', {})
            else:
                return Result.error('链接错误')

        else:
            return Result.error('链接错误')

# 修改密码
class changePwdView(View):
    def post(self,request):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email_code = request.POST.get('code')
        all_records = EmailVerifyRecord.objects.filter(code=email_code,send_type='forget',is_valid=0,send_time__gte=datetime.now()-timedelta(minutes=30))
        if all_records:
            for record in all_records:
                if password1 == password2:
                    # 已使用状态置为1
                    record.is_valid = 1
                    email = record.email
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    user.save()
                    record.save()
                    return Result.success()
                else:
                    return Result.error('密码不一致')
        else:
            return Result.error('链接错误')



