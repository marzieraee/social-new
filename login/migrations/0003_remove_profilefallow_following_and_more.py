# Generated by Django 4.0.6 on 2022-10-17 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_alter_profilefallow_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilefallow',
            name='following',
        ),
        migrations.RemoveField(
            model_name='profilefallow',
            name='myprofile',
        ),
        migrations.AddField(
            model_name='profilefallow',
            name='from_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profilefallow',
            name='to_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]