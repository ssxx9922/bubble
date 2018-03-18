from datetime import datetime

from django.db import models

# Create your models here.

class crawlState(models.Model):
    target = models.CharField(max_length=100,verbose_name='爬取目标网站',default='')
    state = models.CharField(choices=(('success','成功'),('failure','失败'),('default','默认')),default='default',max_length=10,verbose_name='状态')
    note = models.TextField(verbose_name='备注',default='')
    crawltime = models.DateTimeField(default=datetime.now, verbose_name='爬取时间')
    completetime = models.CharField(max_length=20,verbose_name='爬取用时')

    def __str__(self):
        return self.target

    class Meta:
        verbose_name = '爬取列表'
        verbose_name_plural = verbose_name