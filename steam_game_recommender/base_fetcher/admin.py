from django.contrib import admin
from base_fetcher.models import SteamUser, SteamGame, SteamUserGame

# Register your models here.

class SteamUserAdmin(admin.ModelAdmin):
	pass

class SteamGameAdmin(admin.ModelAdmin):
	pass

class SteamUserGameAdmin(admin.ModelAdmin):
	pass

admin.site.register(SteamUser, SteamUserAdmin)
admin.site.register(SteamGame, SteamGameAdmin)
admin.site.register(SteamUserGame, SteamUserGameAdmin)
