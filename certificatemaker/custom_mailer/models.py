from django.db import models

# Create your models here.


from certificatestore.models import Certificate



class Message(models.Model):
    slug = models.CharField(max_length=200,blank=True)
    subject = models.CharField(max_length=200,blank=True)
    body = models.TextField()
    email_from = models.CharField(max_length=254)
    reply_to = models.EmailField(max_length=254)
    bcc_email = models.EmailField(max_length=254)
    from_name = models.CharField(max_length=254)


class MessageStatus(models.Model):
    email_to = models.EmailField(max_length=254)
    result_id = models.CharField(max_length=200,blank=True)
    result_status = models.CharField(max_length=200,blank=True)
    certificate = models.ForeignKey('certificatestore.Certificate', on_delete=models.SET_NULL, blank=True, null=True)



