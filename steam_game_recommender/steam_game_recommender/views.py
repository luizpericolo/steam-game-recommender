# -*- coding: utf-8 -*-
from utils import SteamIdConverterCrawler
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from steam_game_recommender.forms import SteamGameRecommenderForm

def initial(request):
	form = SteamGameRecommenderForm()
	return TemplateResponse(request, 'index.html', {'form': form})

def get_recommendation(request):
	import json, re
	import graphlab as gl
	from django.conf import settings
	from utils import SteamWishlistFetcher, FriendListFetcher

	steam_name = request.POST['steam_name']

	if re.compile(r"\d+").match(steam_name):
		steam_id = steam_name

	crawler = SteamIdConverterCrawler()
	steam_id = crawler.get_steamid64(steam_name=steam_name)

	friendListFetcher = FriendListFetcher(app_key=settings.API_KEY)
	friends = friendListFetcher.get_friends(steamid=steam_id)

	# Gerar a base a partir dos ids dos amigos e jogar para o
	# graphlab.
	games = open("./games_list.json", 'r')
	games_list = json.load(games)
	games.close()

	data = gl.SFrame.read_csv("./scored_output.csv",column_type_hints={"score": int})

	# Definindo para quem devemos fazer sugestões
	users = [steam_id]

	model = gl.recommender.create(data, user_id="steam_id", item_id="app_id", target="score")
	#model = gl.ranking_factorization_recommender.create(data, user_id="steam_id", item_id="app_id", target="score")
	recommended_games = model.recommend(users=users, k=5)

	games = []

	for game in recommended_games:
		game = {
			'name': games_list[game.get('app_id')],
			'url': "http://store.steampowered.com/app/{}".format(game.get('app_id')),
			'score': game.get('score')
		}
		games.append(game)

	wishlistFetcher = SteamWishlistFetcher()
	wishlist_games = wishlistFetcher.retrieve_wishlist_for_steam_id(steam_id=steam_id)

	ctx = {'steam_name': request.POST['steam_name'], 'games': games, "wishlist_games": wishlist_games}

	return TemplateResponse(request, 'results.html', ctx)
