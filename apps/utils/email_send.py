#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/3/26 PM3:22'

from random import Random
from django.core.mail import send_mail
from user.models import EmailVerifyRecord
from bubble.settings import EMAIL_HOST_USER,REQUEST_URL

def random_str(randomlength=8):
    str = ''
    chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '注册激活链接'
        email_body = '点击下面的链接激活你的账号：{0}/user/active/{1}\n(30分钟内有效)'.format(REQUEST_URL,code)
        send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '重置密码'
        email_body = '点击下面的链接重置密码：{0}/user/reset/{1}\n(30分钟内有效)'.format(REQUEST_URL,code)
        send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email])
        if send_status:
            pass

def send_email(email_title,email_body,email):
    send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, email)
    if send_status:
        pass