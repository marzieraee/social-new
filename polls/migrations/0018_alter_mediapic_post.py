# Generated by Django 4.1 on 2022-08-15 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_cptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediapic',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pic', to='polls.mypost'),
        ),
    ]