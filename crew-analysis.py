import argparse
import json
import logging

def read_json_to_dict(file_name):
    pass

def read_txt_to_list(file_name):
    pass


"""
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
    my_crew = read_txt_to_list(args.my_crew_file)


"""
"""
if __name__ == '__main__':
    # Set up args
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
        choices=['overview', 'best-stats', 'prestige'], 
        help='The analysis mode to perform')
    
    args = parser.parse_args()
    main(args)