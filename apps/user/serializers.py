#_*_ coding:utf-8 _*_
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from user.models import EmailVerifyRecord

__author__ = 'Harryue'
__date__ = '2018/5/8 PM3:54'

from rest_framework import serializers

User = get_user_model()

class CodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        """
        验证邮箱
        :param email: 
        :return: 
        """
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError('用户已经注册')

        one_minte_ago = datetime().now() - timedelta(hours=0,minutes=30,seconds=0)
        if EmailVerifyRecord.objects.filter(send_time__gt=one_minte_ago,email=email):
            raise serializers.ValidationError('请查阅你邮箱中的激活邮件')

        return email

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fileds = ('username','code')