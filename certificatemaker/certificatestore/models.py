from django.db import models

# Create your models here.


def set_path_and_filename(instance, filename):
    return '/'.join(['certificates', instance.filename])


class Certificate(models.Model):
    upload = models.FilePathField(editable=False)
    #upload = models.FileField(upload_to=set_path_and_filename, blank=True, null=True)
    filename = models.CharField(max_length=200,editable=False,blank=False)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    parent_record = models.ForeignKey('preprintrecorder.PrePrintRecord', editable=False, on_delete=models.SET_NULL, null=True)
    latex_process = models.ForeignKey('latexprocessor.LatexProcess', editable=False, on_delete=models.SET_NULL, null=True)
    orgy = models.ForeignKey('CertificateOrgy', on_delete=models.SET_NULL, null=True,editable=False)




class CertificateOrgy(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return  str(self.created)

