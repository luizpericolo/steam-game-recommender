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

	community_data = gl.SFrame.read_csv("./steam_base.csv",column_type_hints={"score": int})

	print "amigos: {}".format(friends)

	friends_data = community_data.filter_by(friends, 'steam_id')

	# Definindo para quem devemos fazer sugestões
	users = [steam_id]

	#community_model = gl.recommender.create(community_data, user_id="steam_id", item_id="app_id", target="score")
	community_model = gl.recommender.ranking_factorization_recommender.create(community_data, user_id="steam_id", item_id="app_id", target="score")
	#community_model = gl.recommender.factorization_recommender.create(community_data, user_id="steam_id", item_id="app_id", target="score")
	#community_model = gl.recommender.item_similarity_recommender.create(community_data, user_id="steam_id", item_id="app_id", target="score")
	community_recommended_games = community_model.recommend(users=users, k=5)

	if friends_data.num_rows():
		print "Quantos amigos na base: {}".format(friends_data.num_rows())
		friends_model = gl.item_similarity_recommender.create(friends_data, user_id="steam_id", item_id="app_id", target="score")
		friends_recommended_games = friends_model.recommend(users=users, k=5)
	else:
		print 'Sem amigos na base :('
		friends_recommended_games = []

	games = []

	for game in community_recommended_games:
		game = {
			'name': games_list[game.get('app_id')],
			'url': "http://store.steampowered.com/app/{}".format(game.get('app_id')),
			'score': game.get('score')
		}
		games.append(game)
	
	friends_games = []

	for game in friends_recommended_games:
		game = {
			'name': games_list[game.get('app_id')],
			'url': "http://store.steampowered.com/app/{}".format(game.get('app_id')),
			'score': game.get('score')
		}

		friends_games.append(game)

	wishlistFetcher = SteamWishlistFetcher()
	wishlist_games = wishlistFetcher.retrieve_wishlist_for_steam_id(steam_id=steam_id)

	ctx = {
		'steam_name': request.POST['steam_name'],
		'games': games,
		'friends_games': friends_games,
		"wishlist_games": wishlist_games,
	}

	return TemplateResponse(request, 'results.html', ctx)
