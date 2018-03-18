from django.urls import path
from information.views import ListView,InteractView,coinList,coinOnly

urlpatterns = [
    path('list', ListView.as_view()),
    path('touch', InteractView.as_view()),
    path('coinList', coinList.as_view()),
    path('coinOnly', coinOnly.as_view())
]