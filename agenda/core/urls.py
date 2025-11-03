from django.urls import path
from core.views import login, logout, home, create_contact, list_contacts, update_contact, delete_contact


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('', home, name='home'),
    path('contacts/create/', create_contact, name='create_contact'),
    path('contacts/', list_contacts, name='list_contacts'),
    path('contacts/<int:contact_id>/update/', update_contact, name='update_contact'),
    path('contacts/<int:contact_id>/delete/', delete_contact, name='delete_contact'),
]