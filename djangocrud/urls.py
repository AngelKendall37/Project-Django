"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from activity import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= 'home'),
    path('signup/', views.signup, name= 'signup'),
    path('activity/', views.activity, name= 'activity'),
    path('activity_completed/', views.activity_completed, name= 'activity_completed'),
    path('activity/create/', views.create_activity, name= 'create_activity'),
    path('activity/<int:activity_id>/', views.activity_detail, name= 'activity_detail'),
    path('activity/<int:activity_id>/complete/', views.complete_activity, name= 'complete_activity'),
    path('activity/<int:activity_id>/delete/', views.delete_activity, name= 'delete_activity'),
    path('logout/', views.signout, name= 'logout'),
    path('signin/', views.signin, name= 'signin'),
  
]
