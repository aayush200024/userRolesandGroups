from django.urls import path
from . import views

urlpatterns = [
    path('manage_roles/<int:user_id>/', views.manage_roles, name='manage_roles'),
    path('user_list/', views.user_list, name='user_list'),
    path('', views.manage_users, name='manage_users'),

]
