from django.urls import path
from . import views

app_name = 'guias'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('locator/', views.locator, name='locator'),
    path('process_addresses/', views.process_addresses, name='process_addresses'),
    path('address_return/', views.address_return, name='address_return'),  # Adicionada a nova URL
]
