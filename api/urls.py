from django.urls import path
from .views import (
    register_user, login_user, add_contact, edit_contact, 
    get_contacts, get_contact_by_id
)

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('contacts/', get_contacts, name='get_contacts'),
    path('contacts/add/', add_contact, name='add_contact'),
    path('contacts/<int:contact_id>/', get_contact_by_id, name='get_contact_by_id'),
    path('contacts/<int:contact_id>/edit/', edit_contact, name='edit_contact'),
]
