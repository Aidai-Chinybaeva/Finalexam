from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view()),
    path('staff/', views.StaffRegisterAPIView.as_view()),
    path('admin/', admin.site.urls),
]