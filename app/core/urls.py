"""URLS Mapping for the Core API"""
from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('pins/', views.PINListCreateAPIVIew.as_view(), name='pins')
]
