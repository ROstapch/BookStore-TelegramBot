# Generated by Django 2.2.7 on 2019-11-23 14:31

import Store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='photo',
            field=models.ImageField(upload_to=Store.models.get_image_path),
        ),
    ]
