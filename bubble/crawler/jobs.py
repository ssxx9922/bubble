#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/3/16 PM3:39'

import time
from datetime import datetime
from crawler.views import crawl
from crawler.models import crawlState
from django.core.mail import send_mail

def crawlJob():
    print('1')
    crawlObj = crawl()
    crawlObj.crawlerBshijie()
    crawlObj.crawlerJinse()
    crawlObj.crawlerWallstreetcn()
    crawlObj.crawlerBiknow()


def reportJob():
    y = time.strftime("%Y", time.localtime(time.time()))
    m = time.strftime("%m", time.localtime(time.time()))
    d = time.strftime("%d", time.localtime(time.time()))
    fd = time.strftime("%d", time.localtime(time.time()-86400))
    date_from = datetime(int(y), int(m), int(fd), 0, 0)
    date_to = datetime(int(y), int(m), int(d), 0, 0)
    list = crawlState.objects.filter(crawltime__range=(date_from, date_to))
    successList = list.filter(state='success')
    failureList = list.filter(state='failure')

    lenSuccess = len(successList)
    lenFailure = len(failureList)

    mailData = '总数:{all}\n成功数:{succ}\n失败数:{fail}'.format(all=len(successList),succ=lenSuccess,fail=lenFailure)

    send_mail('爬取信息', mailData, 'ssxx9922@163.com', ['andy.shi@foxmail.com'], fail_silently=False)

    print('2')