from django.db import models
from django.urls import reverse

from users.models import User, Registrar
from django.core.mail import send_mail
from CUNYzero import settings


# Create your models here.
class Warnings(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, primary_key=False, null=True)
    registrar = models.ForeignKey(Registrar, on_delete=models.CASCADE, unique=False, primary_key=False, null=True)
    description = models.CharField(max_length=30, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.user.__str__() + " - " + self.description.__str__()

    def send_warning(self, msg):
        send_mail(
            subject='CUNYZero - Warning:',
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email])

    def get_absolute_url(self):
        return reverse('warning_details', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('remove_warning', kwargs={'pk': self.id})
