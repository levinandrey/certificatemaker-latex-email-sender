from django.db import models

# Create your models here.

#from latexprocessor.models import LatexProcess


class PrePrintRecord(models.Model):
    last_name = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    second_name = models.CharField(max_length=100, blank=True,)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    attrs = models.CharField(max_length=300)
    process = models.ForeignKey('latexprocessor.LatexProcess', on_delete=models.SET_NULL, blank=True, null=True)
    gen_cert = models.BooleanField(default=False)

    GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('u', 'undefined'),
        ('', 'none'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, null=True,blank=True,)

    #latex_document = models.CharField(max_length=100, editable=False)

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' +self.second_name