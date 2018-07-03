# Generated by Django 2.0.6 on 2018-07-03 16:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sani_optika', '0010_remove_review_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('starts', models.CharField(max_length=10)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sani_optika.Location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sani_optika.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='location',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]
