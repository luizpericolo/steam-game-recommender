# -*- coding: utf-8 -*-
from utils import SteamIdConverterCrawler
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from steam_game_recommender.forms import SteamGameRecommenderForm

def initial(request):
	form = SteamGameRecommenderForm()
	return TemplateResponse(request, 'index.html', {'form': form})

def get_recommendation(request):
	from utils import SteamWishlistFetcher
	steam_name = request.POST['steam_name']
	crawler = SteamIdConverterCrawler()
	steam_id = crawler.get_steamid64(steam_name)

	wishlistFetcher = SteamWishlistFetcher()
	wishlist_games = wishlistFetcher.retrieve_wishlist_for_steamname(steamname=steam_name)

	games = [
		{'name': 'Counter-Strike','url':'http://store.steampowered.com/app/10'},
		{'name': 'BioShock' ,'url': 'http://store.steampowered.com/app/7670'},
		{'name': 'Half-Life 2','url': 'http://store.steampowered.com/app/220'},
	]

	return TemplateResponse(request, 'results.html', {'steam_name': request.POST['steam_name'], 'games': games, "wishlist_games": wishlist_games})
