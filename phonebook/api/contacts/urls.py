from django.urls import path

from .views import (
    ContactListAPI,
    ContactCreateAPI,
    ContactDeleteAPI,
)

urlpatterns = [
    path('list/', ContactListAPI.as_view(), name='contact-list'),
    path('add/', ContactCreateAPI.as_view(), name='contact-add'),
    path('delete/', ContactDeleteAPI.as_view(), name='contact-delete'),
]
