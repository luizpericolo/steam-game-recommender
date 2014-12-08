# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    help = u"Recupera o nome do jogo a partir de um arquivo json."
    args = "<file>"

    option_list = BaseCommand.option_list + (
        make_option('--file',
            action='store',
            dest='file',
            help="Caminho do arquivo json a ser transformado"
        ),
    )

    def handle(self, *args, **options):
        import json, time

        start = time.time()
        count = 0

        file_p = open(options.get('file'), 'r')
        json_data = json.load(file_p)
        file_p.close()
        
        count = len(json_data)

        json_file = open("games_list.json", 'w')

        games = {}

        for i, data in enumerate(json_data):
            if not data.get('app_id') in games:
                games[data.get('app_id')] = data.get('app_name')
            print u"{:.2f}% processed...".format((100.0*i)/count)
            
        with open('games_list.json', 'w') as json_games:
            json.dump(games, json_games)

        end = time.time()

        print u"{} entries processed in {:.2f} seconds".format(count, end-start)