# Generated by Django 3.2.12 on 2022-03-13 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220310_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.ImageField(blank=True, max_length=3, null=True, upload_to=''),
        ),
    ]
