# Generated by Django 2.1.5 on 2019-04-12 16:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(-1, '#ff6666'), (0, '#ff6666'), (1, 'white')]),
        ),
        migrations.AlterField(
            model_name='task',
            name='timestamp',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]
