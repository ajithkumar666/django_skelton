from django.urls import path

from user.views import UserView

urlpatterns = [
    path('test',view=UserView.test, name="test"),
    path('llama',view=UserView.llama, name="llama"),
]