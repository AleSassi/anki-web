from django.core.files.storage import FileSystemStorage
from django.db import models
from django import forms

fs = FileSystemStorage(location="media/files/")

class CollectionModel(models.Model):
    title = forms.CharField(max_length=50)
    file = forms.FileField(storage=fs)
