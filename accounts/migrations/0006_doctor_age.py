# Generated by Django 3.2.12 on 2022-03-23 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220319_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]