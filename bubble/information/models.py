from datetime import datetime
from django.db import models

# Create your models here.



class information(models.Model):
    info = models.TextField(verbose_name='信息')
    author = models.CharField(max_length=20, verbose_name='来源', default='')
    infotime = models.DateTimeField(default=datetime.now(),verbose_name='加入时间')
    infoid = models.CharField(max_length=20, verbose_name='信息ID')

    def __str__(self):
        return self.info

    class Meta:
        verbose_name = '信息流'
        verbose_name_plural = verbose_name

