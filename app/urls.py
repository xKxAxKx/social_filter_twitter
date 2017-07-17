from django.conf.urls import url
from django.conf import settings
from app import views

urlpatterns = [
    url(r'^home/', views.home.as_view(), name='home'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^', views.index.as_view(), name='index'),
]
