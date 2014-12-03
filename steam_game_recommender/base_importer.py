import json, time

from base_fetcher.models import *
start = time.time()
json_data = open('steamcommunity.json')
data = json.load(json_data)
json_data.close()

total = len(data)
processed = 0

print "{}% importados...".format((100.0*processed/total))

for entry in data:
    steam_user = SteamUser.objects.filter(steamid=entry.get('steam_id'))

    if not steam_user:
        steam_user = SteamUser.objects.create(steamid=entry.get('steam_id'))
    else:
        steam_user = steam_user[0]

    steam_game = SteamGame.objects.filter(appid=entry.get('app_id'))

    if not steam_game:
        steam_game = SteamGame.objects.create(appid=entry.get('app_id'), name=entry.get('app_name'))
    else:
        steam_game = steam_game[0]

    steam_user_game = SteamUserGame.objects.filter(user=steam_user, game=steam_game)

    if not steam_user_game:
        total_hours_played = entry.get('total_hours_played').replace(",", ".")
        achievements_percentage = entry.get('achievements_percentage').replace(",", ".")
        steam_user_game = SteamUserGame.objects.create(user=steam_user, game=steam_game, total_hours_played=total_hours_played, achievements_percentage=achievements_percentage)
        processed += 1


    print "{}% importados...".format((100.0*processed/total))

end = time.time()

print "{} pares importados em {} segundos".format(SteamUserGame.objects.count(), int(end-start))


