from django.contrib import admin
from django.urls import path, include
from tracker import views as tracker_views
from django.contrib.auth import views as auth_views
from django.urls import path
from tracker import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tracker_views.home, name='home'),
    path('add/', tracker_views.add_activity, name='add_activity'),
    path('register/', tracker_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='tracker/logout.html'), name='logout'),
    path('delete/<int:pk>/', tracker_views.delete_activity, name='delete_activity'),
    path('test-db/', views.test_db, name='test_db'),


]
