class SteamIdConverterCrawler():
	def __init__(self):
		self.url = "http://steamidconverter.com/{}"

	def _search_for(self, steam_name):
		import urllib2

		lookup_url = self.url.format(steam_name)

		response = urllib2.urlopen(lookup_url)
		return response.read()

	def get_steamid64(self, steam_name):
		from bs4 import BeautifulSoup
		html = self._search_for(steam_name=steam_name)
		soup = BeautifulSoup(html)
		return soup.find("h2", id="steamID64").get_text()

class SteamWishlistFetcher():
	def __init__(self):
		self.url = "http://steamcommunity.com/{}/wishlist"
		self.steam_name_prefix = "id/{}"
		self.steam_id_prefix = "profiles/{}"

	def _retrieve_wishlist(self, url):
		import urllib2
		from bs4 import BeautifulSoup

		response = urllib2.urlopen(url)
		soup = BeautifulSoup(response.read())

		games_html = soup.find_all("div", {"class", "wishlistRow"})

		wishlist = []
		for game_html in games_html:
			wishlist_item = {}
			game_logo = game_html.find("div", {"class": "gameLogo"})
			wishlist_item['game_url'] = game_logo.find("a").get("href").replace("steamcommunity", "store.steampowered")
			wishlist_item['game_image_url'] = game_logo.find("img").get("src")
			wishlist_item['game_name'] = game_html.find("h4").get_text()
			wishlist.append(wishlist_item)

		return wishlist

	def retrieve_wishlist_for_steamname(self, steamname, k=None):
		identifier = self.steam_name_prefix.format(steamname)
		url = self.url.format(identifier)

		if k:
			return self._retrieve_wishlist(url=url)[:k]	
		else:
			return self._retrieve_wishlist(url=url)

	def retrieve_wishlist_for_steam_id(self, steam_id, k=None):
		identifier = self.steam_id_prefix.format(steam_id)
		url = self.url.format(identifier)

		if k:
			return self._retrieve_wishlist(url=url)[:k]
		else:
			return self._retrieve_wishlist(url=url)

class FriendListFetcher():
    def __init__(self, app_key):
        self.app_key = app_key
        self.friend_list_url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key="+app_key+"&steamid={}&relationship=friend"

    def _create_request_session(self, max_retries):
        import requests

        s = requests.Session()
        a = requests.adapters.HTTPAdapter(max_retries=max_retries)
        b = requests.adapters.HTTPAdapter(max_retries=max_retries)

        s.mount("http://", a)
        s.mount("https://", b)
        return s
    
    def get_friends(self, steamid):
        import requests
        #import pudb; pu.db
        url = self.friend_list_url.format(steamid)
        session = self._create_request_session(max_retries=10)  
         
        response = session.get(url)
        return map(lambda friend: friend['steamid'],response.json()['friendslist']['friends'])