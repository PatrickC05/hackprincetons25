# Generated by Django 5.1 on 2025-03-29 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_matchup_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchup',
            name='in_progress',
            field=models.BooleanField(default=True),
        ),
    ]
