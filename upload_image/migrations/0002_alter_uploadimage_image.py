# Generated by Django 3.2.12 on 2022-03-24 14:08

from django.db import migrations, models
import upload_image.models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_image', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadimage',
            name='image',
            field=models.ImageField(upload_to=upload_image.models.path_and_rename, verbose_name='Upload Image'),
        ),
    ]
