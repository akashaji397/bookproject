
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("create-book/", views.createBook, name='createBook'),
    path("author/", views.CreateAuthor, name='author'),
    path("listbook/", views.listBook, name='listBook'),
    path('detailsview/<int:book_id>/', views.detailsview, name='details'),
    path("updatebook/<int:book_id>/", views.updatebook, name='update'),
    path('deletebook/<int:book_id>/', views.deletebook, name='delete'),
    path('index',views.index),
    path('search/',views.Search_Book,name='search'),
    path('admin_view/',views.admin_view,name='admin_view'),

    
]
