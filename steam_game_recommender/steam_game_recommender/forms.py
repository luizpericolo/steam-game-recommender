from django import forms

class SteamGameRecommenderForm(forms.Form):
	steam_name = forms.CharField(label='Steam Name', max_length=255)