# Generated by Django 4.1 on 2022-08-10 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_alter_mediapeofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediapeofile',
            name='image',
            field=models.ImageField(default='profile/x22.png', upload_to='profile/'),
        ),
    ]
