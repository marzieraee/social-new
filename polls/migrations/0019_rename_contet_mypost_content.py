# Generated by Django 4.1 on 2022-08-15 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_alter_mediapic_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mypost',
            old_name='contet',
            new_name='content',
        ),
    ]