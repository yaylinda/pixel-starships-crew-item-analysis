import argparse
import json
from collections import OrderedDict
import requests

def read_json_to_dict(file_name):
    print('Reading data from file: %s' % file_name)
    data = json.load(open(file_name))
    print('\tLoaded %d datum from file into dict' % len(data))

    transformed = {}
    for d in data.keys():
        transformed[data[d]['name'].lower()] = data[d]

    return transformed


def read_txt_to_list(file_name):
    print('Reading user-data from file: %s' % file_name)
    items = [line.rstrip('\n').lower() for line in open(file_name)]
    print('\tLoaded %d items from file into list' % len(items))
    return items


def parse_crew_list(crew_data, my_crew_list):
    parsed = []
    not_found = []

    for c in my_crew_list:
        if c in crew_data:
            parsed.append(crew_data[c])
        else:
            not_found.append(c)

    print('Parsed %d out of %d in the given crew list' % (len(parsed), len(my_crew_list)))
    print('%d unknown crew: ' % len(not_found))
    for c in not_found:
        print('\t%s' % c)

    return parsed


def print_stat_map(name, stat_map):
    print('--------------------')
    print(name)
    print('--------------------')

    for s in stat_map.keys():
        print(s)
        for c in stat_map[s]:
            print('\t%s' % c)


def compute_overview(crew_data, item_data, my_crew):
    print('Computing analysis for OVERVIEW...')

    # group by collection
    collection = {}
    for c in my_crew:
        x = c['collection_name']
        if len(x) == 0:
                x = 'NONE'
        if x not in collection:
            collection[x] = []
        collection[x].append(c['name'])
    print_stat_map('COLLECTION', collection)

    # group by rarity
    rarity = {}
    for c in my_crew:
        x = c['rarity']
        if x not in rarity:
            rarity[x] = []
        rarity[x].append(c['name'])
    print_stat_map('RARITY', rarity)

    # group by ability
    ability = {}
    for c in my_crew:
        x = c['special_ability']
        if x not in ability:
            ability[x] = []
        ability[x].append(c['name'])
    print_stat_map('ABILITY', ability)

    # group by best hp
    hp = {}
    for c in my_crew:
        x = c['hp'][1]
        if x not in hp:
            hp[x] = []
        hp[x].append(c['name'])
    print_stat_map('HP', OrderedDict(sorted(hp.items(), key=lambda t: t[0])))

    # group by best attack
    attack = {}
    for c in my_crew:
        x = c['attack'][1]
        if x not in attack:
            attack[x] = []
        attack[x].append(c['name'])
    print_stat_map('ATTACK', OrderedDict(sorted(attack.items(), key=lambda t: t[0])))

    # group by best ability num
    ability_val = {}
    for c in my_crew:
        x = c['ability'][1]
        if x not in ability_val:
            ability_val[x] = []
        ability_val[x].append(c['name'])
    print_stat_map('ABILITY STAT', OrderedDict(sorted(ability_val.items(), key=lambda t: t[0])))

    # group by best pilot
    pilot = {}
    for c in my_crew:
        x = c['pilot'][1]
        if x not in pilot:
            pilot[x] = []
        pilot[x].append(c['name'])
    print_stat_map('PILOT', OrderedDict(sorted(pilot.items(), key=lambda t: t[0])))

    # group by best science
    science = {}
    for c in my_crew:
        x = c['science'][1]
        if x not in science:
            science[x] = []
        science[x].append(c['name'])
    print_stat_map('SCIENCE', OrderedDict(sorted(science.items(), key=lambda t: t[0])))

    # group by best engineer
    engineer = {}
    for c in my_crew:
        x = c['engine'][1]
        if x not in engineer:
            engineer[x] = []
        engineer[x].append(c['name'])
    print_stat_map('ENGINEER', OrderedDict(sorted(engineer.items(), key=lambda t: t[0])))

    # group by best weapon
    weapon = {}
    for c in my_crew:
        x = c['weapon'][1]
        if x not in weapon:
            weapon[x] = []
        weapon[x].append(c['name'])
    print_stat_map('WEAPON', OrderedDict(sorted(weapon.items(), key=lambda t: t[0])))


def compute_prestige_options(crew_data, item_data, my_crew):
    print('Computing analysis for PRESTIGE OPTIONS')

    my_crew_ids = {}
    for c in my_crew:
        my_crew_ids[c['id']] = c['name']

    legendaries = []
    for c in crew_data.keys():
        if crew_data[c]['rarity'] == 'legendary':
            legendaries.append({"id": crew_data[c]['id'], "name": crew_data[c]['name']})

    combos = []
    for legend in legendaries:
        url = 'http://www.pixyship.com/api/prestige/' + str(legend['id'])
        print('getting prestige info for %s from %s' % (legend['name'], url))
        response = requests.get(url)
        prestige_data = response.json()['data']['to'] # map of id:[id]
        for id in prestige_data.keys():
            if (int(id) in my_crew_ids):
                for with_id in prestige_data[id]:
                    if (with_id in my_crew_ids):
                        combos.append({"id1": int(id), "id2": with_id, "result": legend['name']})

    for combo in combos:
        print('%s + %s = %s' % (my_crew_ids[combo['id1']], my_crew_ids[combo['id2']], combo['result']))


def compute_best_stats(crew_data, item_data, my_crew):
    print('Computing analysis for BEST STATS...')
    # TODO


"""
Read data and user data from files.
Call correct method to do analysis based on input mode.
"""
def main(args):
    print('Starting analysis with params:')
    print('\tcrew_data_file = %s' % args.crew_data_file)
    print('\titem_data_file = %s' % args.item_data_file)
    print('\tmy_crew_file = %s' % args.my_crew_file)
    print('\tmode = %s' % args.mode)
    print('\n')

    crew_data = read_json_to_dict(args.crew_data_file)
    item_data = read_json_to_dict(args.item_data_file)
    my_crew_list = read_txt_to_list(args.my_crew_file)
    print('\n')

    my_crew_data = parse_crew_list(crew_data, my_crew_list)
    print('\n')

    if (args.mode == 'overview'):
        compute_overview(crew_data, item_data, my_crew_data)
        return
    if (args.mode == 'stats'):
        compute_best_stats(crew_data, item_data, my_crew_data)
        return
    if (args.mode == 'prestige'):
        compute_prestige_options(crew_data, item_data, my_crew_data)
        return


"""
Parse arguments and call main()
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze Pixel Starship crew and items')
    parser.add_argument('--crew-data-src', 
        dest='crew_data_file', 
        default='data/crew.json', 
        help='The source file for crew data')
    parser.add_argument('--item-data-src', 
        dest='item_data_file', 
        default='data/items.json', 
        help='The source file for item data')
    parser.add_argument('--my-crew-src', 
        dest='my_crew_file', 
        default='user-data/my-crew.txt', 
        help='The file containing crew names, one name per line')
    parser.add_argument('--mode', 
        dest='mode', 
        required=True, 
        choices=['overview', 'stats', 'prestige'], 
        help='The analysis mode to perform')
    
    args = parser.parse_args()
    main(args)