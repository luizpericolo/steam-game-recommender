# -*- coding: utf-8  -*-
from django.db import models

# Create your models here.

class SteamUser(models.Model):
	# SteamID do usuário
	steamid = models.IntegerField(null=False)

class SteamGame(models.Model):
	# AppID do jogo na steam
	appid = models.IntegerField(null=False)
	
	# Nome do jogo na Steam
	name = models.CharField(max_length=255)

class SteamUserGame(models.Model):

    # Chave estrangeira para o Usuário da Steam
    user = models.ForeignKey('SteamUser', null=False)
    
    # Chave estrangeira para o Jogo da Steam
    game = models.ForeignKey('SteamGame', null=False)
    
    # Quantidade de horas jogadas pelo user
    total_hours_played = models.FloatField(null=False)
    
    # Percentagem de achievements conquistados pelo user
    achievements_percentage = models.FloatField(null=False)
