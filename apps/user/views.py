from django.shortcuts import render

# Create your views here.
from django.views import View

# 登录
class loginView(View):
    def psot(self,request):
        pass

# 注册
class registerView(View):
    def post(self, request):
        pass

# 激活邮箱
class activeView(View):
    def post(self, request, active_code):
        pass

# 忘记密码
class forgetPwdView(View):
    def post(self,request):
        pass

#重置密码
class resetView(View):
    def post(self,request, active_code):
        pass