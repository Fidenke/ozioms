from django.urls import path
from . import views

urlpatterns = [
  path(
    '', 
    views.home, 
    name='home'
  ),
  path(
    'contact', 
    views.contact, 
    name='contact'
  ),
  path(
    'signup', 
    views.signupView, 
    name='signup'
  ),
  path(
    'login',
    views.loginView,
    name='login'
  ),
  path('privacy',
    views.privacy,
    name='privacy'
  ),
  path('terms',
    views.terms,
    name='terms'
  ),

  path(
    'logout',
    views.logoutView,
    name='logout'
  ),
]