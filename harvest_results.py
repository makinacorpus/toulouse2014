#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collections import namedtuple
import csv
import json
import sys
import requests
from pyquery import PyQuery as pq


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
OfficeResults = namedtuple(
    'OfficeResult',
    'name, associant, ' + ' ,'.join(candidates))
#HARVEST_URL = "http://rbv.toulouse.fr/resultats/resultats_par_bureau_vote.php"
HARVEST_URL = "http://rbv.toulouse.fr/resultats/ws_resultats_bv.php"
SCRUTIN = "7"

harvest_order = ['']


def get_percent(ind, element):

    print pq(element).eq(0)


def get_result(ind, element):

    td_element = pq(element).find('td')
    print(td_element)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        msg = 'Usage : {command} <file.csv> <fileout.json>'.format(
            command=sys.argv[0])
        print(msg)
        exit()

    #response = requests.get(HARVEST_URL, params={'scrutin': 7,
    #                                             'idNumBV3': num_vote})

    #print(response.content)

    json_content = {}

    with open(sys.argv[1], 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        # Skipping csv header
        reader.next()

        for row in map(OfficeResults._make, reader):
            formatted_associant = row.associant.rjust(5, '0')

            msg = 'Requesting URL : {url}'.format(
                url="/".join([HARVEST_URL, SCRUTIN, formatted_associant]))
            print(msg)
            response = requests.get(
                HARVEST_URL,
                params={'scrutin': SCRUTIN, 'idNumBV3': formatted_associant})

            json_content[row.associant] = json.loads(response.content)

    with open("results.json", 'w') as outfile:
        response_json = json.dump(json_content, outfile)
