from django.urls import path

from .views import (
    ContactListAPI,
)

urlpatterns = [
    path('', ContactListAPI.as_view(), name='contact-list'),
]
