# Generated by Django 5.1 on 2025-03-29 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_stocks',
            field=models.ManyToManyField(blank=True, related_name='users', to='main.stock'),
        ),
    ]
