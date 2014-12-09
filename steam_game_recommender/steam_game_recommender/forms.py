from django import forms

class SteamGameRecommenderForm(forms.Form):
	steam_name = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'placeholder': 'SteamID or Steam Name...'}))