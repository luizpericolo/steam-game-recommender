# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    help = u"Converte um arquivo csv em um arquivo csv com notas."
    args = "<file>"

    option_list = BaseCommand.option_list + (
        make_option('--file',
            action='store',
            dest='file',
            help="Caminho do arquivo csv a ser transformado"
        ),
    )

    def handle(self, *args, **options):
        import csv, time
        from collections import Counter
        from operator import itemgetter
        from math import ceil

        start = time.time()
        count = 0

        csv_in_file = open(options.get('file'), 'r')

        counts = Counter(csv_in_file.read())
        csv_in_file.close()
        count = counts.get('\n')

        csv_in_file = open(options.get('file'), 'r')
        csvreader = csv.reader(csv_in_file, delimiter=',')

        csv_out_file = open("scored_output.csv", 'a')

        # Pegando a primeira linha do csv original
        cols = csvreader.next()
        cols.pop()
        cols.append('score')
        descriptor_line = ','.join(cols)
        lines = [descriptor_line+'\n']

        processed_data = {}

        current = 0

        for row in csvreader:
            if not row[0] in processed_data:
                processed_data[row[0]] = []

            processed_data[row[0]].append(tuple(row[1:]))

            current += 1

            print u"{:.2f}% processed...".format((100.0*current)/count)

        csv_in_file.close()

        print u"Calculating and writing new csv..."

        # Iterando nos steam_id do csv
        for key in processed_data.keys():
            play_list = processed_data[key]

            #import pudb; pu.db
            games, play_times = zip(*play_list)

            scores = self._get_scores(play_times=play_times)

            play_list = zip(games, scores)

            for play_item in play_list:
                line = "{},{},{}\n".format(key, play_item[0], play_item[1])
                #line = line.encode('utf-8')
                lines.append(line)

        csv_out_file.writelines(lines)
        csv_out_file.close()
        
        end = time.time()

        print u"{} entries processed in {:.2f} seconds".format(count, end-start)


    def _get_scores(self, play_times):
        from math import ceil

        play_times = map(lambda play: float(play), play_times)

        max_play_time = max(play_times)

        return map(lambda play_time: int(ceil(10.0*(play_time/max_play_time))), play_times)

