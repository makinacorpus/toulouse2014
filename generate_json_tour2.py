#!/usr/bin/python
#-*- coding: utf-8 -*-

from collections import namedtuple
import csv
import json
import sys


"""
    Elisabeth Belaubre (soutenue par le Rassemblement citoyen),
    Ahmed Chouki (soutenu par le NPA),
    Pierre Cohen (PS, PCF, PRG, MDC, Parti occitan),
    Serge Laroze (Toulouse Bleu Marine, soutenu par le FN),
    Antoine Maurice (EÉLV),
    Jean-Luc Moudenc (UMP, UDI, Nouveau centre, Modem, MPF),
    Jean-Pierre Plancade (divers, centre gauche),
    Jean-Christophe Sellin (Parti de Gauche-Front de Gauche),
    Sandra Torremocha (Lutte ouvrière),
    Christine de Veyrac (divers, centre droit).
"""
candidates = ['cohen','moudenc']
OfficeResults = namedtuple(
    'OfficeResult',
    'name, associant, ' + ' ,'.join(candidates))


if __name__ == '__main__':

    if len(sys.argv) != 3:
        msg = 'Usage : {command} <input.csv> <output.json>'.format(
            command=sys.argv[0])
        print(msg)
        exit()

    offices = {}
    with open(sys.argv[1], 'r') as csv_file:

        reader = csv.reader(csv_file, delimiter=',')
        # Skipping csv header
        reader.next()

        for row in map(OfficeResults._make, reader):

            # Get results for each political list
            results = sorted(
                [{candidate: getattr(row, candidate)}
                 for candidate in candidates],
                key=lambda k: int(k.values()[0]),
                reverse=True)

            offices[row.associant] = results

    with open(sys.argv[2], 'w') as outfile:
        response_json = json.dump(offices, outfile)
