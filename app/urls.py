from django.conf.urls import url
from django.conf import settings
from app import views

urlpatterns = [
    url(r'^$', views.index.as_view(), name='index'),
    url(r'^logout/$', views.logout, name='logut'),
    url(r'^home/', views.home.as_view(), name='home'),
]
