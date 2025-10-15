from django.urls import path, include

urlpatterns = [
    path('list/', include('phonebook.api.contacts.urls')),
]
