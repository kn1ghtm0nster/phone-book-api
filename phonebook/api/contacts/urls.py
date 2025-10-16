from django.urls import path

from .views import (
    ContactListAPI,
    ContactCreateAPI,
)

urlpatterns = [
    path('list/', ContactListAPI.as_view(), name='contact-list'),
    path('add/', ContactCreateAPI.as_view(), name='contact-add')
]
