from django.conf.urls import url
from django.conf import settings
from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^logout/$', views.logout, name='logout'),
]
