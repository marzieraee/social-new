# Generated by Django 4.0.6 on 2022-09-06 05:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_rename_fallowing_profilefallow_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='profilefallow',
            name='following',
            field=models.ManyToManyField(related_name='fallowing', to=settings.AUTH_USER_MODEL),
        ),
    ]