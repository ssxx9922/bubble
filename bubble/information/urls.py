from django.urls import path
from information.views import ListView,InteractView

urlpatterns = [
    path('list', ListView.as_view()),
    path('touch', InteractView.as_view()),
]