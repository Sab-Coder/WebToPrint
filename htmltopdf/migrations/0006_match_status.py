# Generated by Django 4.2.4 on 2023-09-08 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('htmltopdf', '0005_alter_away_team_player_player_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='status',
            field=models.CharField(default='ongoing', max_length=50),
        ),
    ]