
from django.urls import path

from . import views

urlpatterns = [
    path('get-pdf', views.get_pdf, name='get_pdf'),
    path('get-test-pdf', views.get_test_pdf, name='get_test_pdf'),
]
