# Generated by Django 3.2.7 on 2021-09-27 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(blank=True, choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=200, null=True),
        ),
    ]
