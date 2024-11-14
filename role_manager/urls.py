from django.contrib import admin
from django.urls import path, include
from user_management import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.manage_users_and_groups, name='manage_users_and_groups'),  # Main user and group management page
    path('accounts/', include('django.contrib.auth.urls')),  # Add authentication views
]
