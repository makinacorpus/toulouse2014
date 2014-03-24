#!/usr/bin/env python
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
candidates = ['belaubre', 'chouki', 'cohen', 'laroze', 'maurice', 'moudenc',
              'plancade', 'sellin', 'torremocha', 'deveyrac']
results_ind = [9, 7, 1, 0, 2, 6, 3, 4, 5, 8]
OfficeResults = namedtuple(
    'OfficeResult',
    'name, associant, ' + ' ,'.join(candidates))


if __name__ == '__main__':

    if len(sys.argv) != 4:
        msg = ('Usage : {command} <input.csv> <results.json> '
               '<output.json>').format(command=sys.argv[0])
        print(msg)
        exit()

    offices = {}

    results_file = open(sys.argv[2], 'r')
    results_content = json.loads(results_file.read())

    with open(sys.argv[1], 'r') as csv_file:

        reader = csv.reader(csv_file, delimiter=',')
        # Skipping csv header
        reader.next()

        for row in map(OfficeResults._make, reader):

            # Get results for each political list
            results = []
            for ind, candidate in enumerate(candidates):

                candidate_result = results_content[row.associant][0][results_ind[ind]][0]

                results.append({candidate: candidate_result})

            results = sorted(results,
                             key=lambda k: float(k.values()[0]),
                             reverse=True)

            offices[row.associant] = results

    with open(sys.argv[3], 'w') as outfile:
        response_json = json.dump(offices, outfile)
