from django.urls import path
from information.views import ListView,InteractView,CrawlerView

urlpatterns = [
    path('list', ListView.as_view()),
    path('touch', InteractView.as_view()),
    path('crawler', CrawlerView.as_view())
]