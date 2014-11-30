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

