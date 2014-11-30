from django.conf.urls import patterns, include, url
from django.contrib import admin
from steam_game_recommender.views import initial, get_recommendation

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'steam_game_recommender.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^recommender/$', initial),
    url(r'^get_recommendation$', get_recommendation),
)
