# Generated by Django 2.0.6 on 2018-07-02 16:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sani_optika', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='path',
            new_name='image_path',
        ),
        migrations.AlterField(
            model_name='order',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 2, 18, 24, 48, 56126)),
        ),
    ]
