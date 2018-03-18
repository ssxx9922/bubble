from datetime import datetime
from django.db import models


# Create your models here.



class information(models.Model):
    info = models.TextField(verbose_name='信息')
    author = models.URLField(default='',verbose_name='来源',max_length=50)
    infotime = models.DateTimeField(default=datetime.now,verbose_name='加入时间')
    crawltime = models.DateTimeField(default=datetime.now, verbose_name='爬取时间')
    infoid = models.CharField(max_length=30, verbose_name='信息ID')
    favour = models.IntegerField(default=0, verbose_name='赞成')
    disfavor = models.IntegerField(default=0, verbose_name='不赞成')

    def __str__(self):
        return self.info

    class Meta:
        verbose_name = '信息流'
        verbose_name_plural = verbose_name


class coin(models.Model):
    coinId = models.CharField(verbose_name='币的ID',max_length=30)
    image = models.TextField(verbose_name='图片')
    name = models.CharField(verbose_name='名字',max_length=20)
    marketValue = models.CharField(verbose_name='市值',max_length=20)
    price = models.CharField(verbose_name='价格',max_length=20)
    circulation = models.CharField(verbose_name='成交量',max_length=20)
    crawltime = models.DateTimeField(default=datetime.now, verbose_name='爬取时间')
    crawlfrom = models.CharField(max_length=20,verbose_name='来源',default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '币行情'
        verbose_name_plural = verbose_name