#_*_ coding:utf-8 _*_
__author__ = 'Harryue'
__date__ = '2018/3/15 PM3:57'

from django.urls import path
from crawler.views import CrawlerInfoView,CrawlerCoinView

urlpatterns = [
    path('info', CrawlerInfoView.as_view()),
    path('coin', CrawlerCoinView.as_view())
]