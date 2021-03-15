from django.db import models

# Create your models here.



class Document(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    upload = models.FileField(upload_to='certificate/%Y/%m/')


class HTMLTemplate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    upload = models.FileField(upload_to='html-template/')




