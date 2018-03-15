#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/3/15 PM3:57'

from django.urls import path
from crawler.views import CrawlerView

urlpatterns = [
    path('info', CrawlerView.as_view())
]