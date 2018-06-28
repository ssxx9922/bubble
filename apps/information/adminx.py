#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/6/28 PM3:51'

import xadmin
from information.models import information, coin

class informationAdmin(object):
    list_display = ('info','author','favour','disfavor','infotime')
    list_filter = ('favour','disfavor')

xadmin.site.register(information,informationAdmin)


class coinAdmin(object):
    list_display = ('no', 'name', 'marketCap', 'price', 'change1h', 'change1d', 'change7d')

xadmin.site.register(coin,coinAdmin)