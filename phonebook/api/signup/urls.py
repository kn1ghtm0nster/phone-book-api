from django.urls import path

from .views import (
    SignUpAPIView
)


urlpatterns = [
    path('', SignUpAPIView.as_view(), name='user-signup'),
]
