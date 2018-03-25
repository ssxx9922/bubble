from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    choices_gender = (
        ('male','男'),
        ('demale','女')
    )
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='wow')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(choices=choices_gender,default='male',max_length=10)
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    header_image = models.ImageField(upload_to='image/%Y/%m', default='')


    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username