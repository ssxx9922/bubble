
# Create your views here.
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views import View
# 登录
from apiData.result import Result
from user.forms import LoginForm
from user.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class loginView(View):
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = request.POST.get('username')
            pass_word = request.POST.get('password')
            user = authenticate(username=user_name,
                                password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Result.success()
                else:
                    return Result.error('用户名或密码错误')
            else:
                return Result.error('用户名或密码错误')
        else:
            return Result.error()


# 注册
class registerEmailView(View):
    def post(self, request):
        user_name = request.POST.get('username')
        users = UserProfile.objects.filter(email=user_name)
        if users.filter(is_active=True):
            return Result.error(message='该账号已经注册')
        if users.filter(is_active=False):
            if EmailVerifyRecord.objects.filter(email=user_name,
                                                send_code='register',
                                                is_valid=0,
                                                send_time__gte=datetime.now()-timedelta(minutes=30)):
                return Result.error(message='请查阅你邮箱中的激活邮件')
            else:
                send_register_email(email=user_name, send_type='register')
                return Result.error(message='一封新的激活邮件已经发到你的邮箱')
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
                                            send_code='forget',
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
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                # TODO
                return Result.success(email)
        else:
            return Result.error('链接错误')

class changePwdView(View):
    def post(self,request):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            return Result.success()
        else:
            return Result.error('密码不一致')

