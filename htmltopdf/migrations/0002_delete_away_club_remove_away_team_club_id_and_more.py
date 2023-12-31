# Generated by Django 4.2.4 on 2023-09-07 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('htmltopdf', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Away_club',
        ),
        migrations.RemoveField(
            model_name='away_team',
            name='club_id',
        ),
        migrations.RemoveField(
            model_name='away_team_player',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='away_team_player',
            name='team_id',
        ),
        migrations.RemoveField(
            model_name='club',
            name='admin_id',
        ),
        migrations.RemoveField(
            model_name='matchteam',
            name='match_id',
        ),
        migrations.RemoveField(
            model_name='matchteam',
            name='team_id',
        ),
        migrations.RemoveField(
            model_name='player',
            name='club_id',
        ),
        migrations.RemoveField(
            model_name='team',
            name='club_id',
        ),
        migrations.RemoveField(
            model_name='team_player',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='team_player',
            name='team_id',
        ),
        migrations.DeleteModel(
            name='away_player',
        ),
        migrations.DeleteModel(
            name='away_team',
        ),
        migrations.DeleteModel(
            name='away_team_player',
        ),
        migrations.DeleteModel(
            name='club',
        ),
        migrations.DeleteModel(
            name='match',
        ),
        migrations.DeleteModel(
            name='matchteam',
        ),
        migrations.DeleteModel(
            name='player',
        ),
        migrations.DeleteModel(
            name='team',
        ),
        migrations.DeleteModel(
            name='team_player',
        ),
    ]
