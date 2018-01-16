from django.urls import path

from . import views

urlpatterns = [
    path('list', views.list),
    path('touch', views.interact),
    path('crawler', views.crawler)
]