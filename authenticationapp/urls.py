from . import views
from django.urls import path

urlpatterns = [
    path('register/',views.UserRegistration,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logout,name='logout'),
    path('',views.index,name='index'),
    
]
