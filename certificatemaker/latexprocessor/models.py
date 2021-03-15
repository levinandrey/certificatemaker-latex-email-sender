from django.db import models
# Create your models here.


class LatexProcess(models.Model):
    name = models.CharField(max_length=200)
    template = models.ForeignKey('Template', on_delete=models.SET_NULL, null=True)
    attrs_names = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50,)

    def __str__(self):
        return  self.name



class Template(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    upload = models.FileField(upload_to='templates/')

    def __str__(self):
        return self.upload.name


class Attachment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    upload = models.FileField(upload_to='attachments/')

    def __str__(self):
        return self.upload.name



