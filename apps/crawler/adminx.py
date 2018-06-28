#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/6/28 PM3:57'

import xadmin
from crawler.models import crawlState

class crawlStateAdmin(object):
    list_display = ('target', 'completetime', 'state', 'crawltime')
    list_filter = ('target', 'state')

xadmin.site.register(crawlState,crawlStateAdmin)