# Generated by Django 4.2.1 on 2024-02-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpost', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.AddField(
            model_name='post',
            name='author_id',
            field=models.IntegerField(blank=True, default=0, null=True, unique=True),
        ),
    ]
