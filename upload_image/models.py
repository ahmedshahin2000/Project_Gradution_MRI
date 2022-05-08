
from ast import Return
import uuid
from uuid import uuid4
import os
from django.db import models
from accounts.models import Patient
import time

def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid.uuid4(), extension)


def path_and_rename(instance, filename):
    upload_to = 'img/'
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    #filename = f'{str(time.ctime())}.{ext}'
    # return the whole path to the file
    imgPath = os.path.join(upload_to, filename)
    return imgPath

class UploadImage(models.Model):
    image = models.ImageField('Upload Image', upload_to=path_and_rename)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.image
