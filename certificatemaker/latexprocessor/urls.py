
from django.urls import path

from . import views

urlpatterns = [
    path('get-pdfs', views.get_pdfs, name='get_pdfs'),

]
