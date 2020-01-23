from django.db import models
from django.urls import reverse

# Create your models here.
class Question(models.Model):
    owner = models.CharField(max_length=50, default="ANONIM")
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    file = models.FileField(upload_to='files/q_files', blank=True, null=True)
    qrcode = models.FileField(upload_to='files/qrcode_files', blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    #blank=True, null=True
    #Question_file = models.FileField(upload_to='documents')

    # def get_absolute_url(self):
    #     return reverse('text', args=[str(self.slug)])


class Answer(models.Model):
    owner = models.CharField(max_length=50, default="ANONIM")
    classname = models.CharField(max_length=50, default="ANONIM", blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='files/a_files', blank=True, null=True)
    question_id = models.PositiveIntegerField(blank=True, null=True)

# class Urlinf(models.Model):
#     url_addr = models.CharField(max_length=100, blank=True, null=True)

