from django.db import models
from django.contrib.auth.models import User

class club(models.Model):
    club_id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media', default='defaultclub.jpg')
    
class player(models.Model):
    player_id = models.AutoField(primary_key=True)
    club_id = models.ForeignKey(club, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    matches_played = models.IntegerField()
    goals = models.IntegerField()
    image = models.ImageField(upload_to='media', default='default.jpg')
    
class team(models.Model):
    team_id = models.AutoField(primary_key=True)
    club_id = models.ForeignKey(club, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class team_player(models.Model):
    team_player_id = models.AutoField(primary_key=True)
    team_id = models.ForeignKey(team, on_delete=models.CASCADE)
    player_id = models.ForeignKey(player, on_delete=models.CASCADE)
    
class away_club(models.Model):
    club_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media', default='defaultawayclub.jpg')

class away_player(models.Model):
    player_id = models.AutoField(primary_key=True)
    club_id = models.ForeignKey(away_club, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    matches_played = models.IntegerField()
    goals = models.IntegerField()
    image = models.ImageField(upload_to='media', default='default.jpg')
    
class away_team(models.Model):
    team_id = models.AutoField(primary_key=True)
    club_id = models.ForeignKey(away_club, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class away_team_player(models.Model):
    team_player_id = models.AutoField(primary_key=True)
    team_id = models.ForeignKey(away_team, on_delete=models.CASCADE)
    player_id = models.ForeignKey(away_player, on_delete=models.CASCADE)
    
class fixture(models.Model):
    match_id = models.AutoField(primary_key=True)
    team_id = models.ForeignKey(team, on_delete=models.CASCADE)
    away_team_id = models.ForeignKey(away_team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=50, default='ongoing')
    