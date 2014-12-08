# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    help = u"Converte um arquivo json em um arquivo csv. Recebe como parâmetro quais chaves do json devem ser convertidas em colunas do csv. Por padrão, todas são convertidas."
    args = "<file col_1 col_2 ...>"

    option_list = BaseCommand.option_list + (
        make_option('--file',
            action='store',
            dest='file',
            help="Caminho do arquivo json a ser transformado"
        ),
        make_option('--cols',
            action='store',
            dest='cols',
            help="Lista de chaves, separadas por virgula, de cada objeto json que será incluída no csv")
    )

    def handle(self, *args, **options):
        import json, time

        start = time.time()
        count = 0

        file_p = open(options.get('file'), 'r')
        json_data = json.load(file_p)
        file_p.close()
        
        count = len(json_data)

        keys = options.get('cols')

        if not keys:
            # Pega todas as chaves do json
            keys = json_data[0].keys()
        else:
            keys = keys.split(',')


        csv_file = open("output.csv", 'w')

        lines = [','.join(keys)+'\n']

        for i, data in enumerate(json_data):
            values = [str(data[key]).replace(',','.') for key in keys]
            line = ','.join(values)+'\n'
            lines.append(line)
            print u"{:.2f}% processed...".format((100.0*i)/count)

        #print map(lambda s: type(s), lines)
        csv_file.writelines(lines)
        csv_file.close()

        end = time.time()

        print u"{} entries processed in {:.2f} seconds".format(count, end-start)

    def _calculate_score(self, entry, keys, expr):

        for key in keys:
            expr = expr.replace(key, str(entry.get(key)))

        # Algumas entradas do json possuem , ao invés de . para designar milhar, milhão, ...
        expr = expr.replace(',','.')
        return eval(expr)
