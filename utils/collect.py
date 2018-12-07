import json
from pprint import pprint
import re
import sys
import getopt

def read_pubs(filenames: list) -> list:
    '''
    Create a list of publications from a set list of filenames.
    It is expected that the publications in the incoming filen
    are in JSON format, like so
    [
        {
            "title": "Some Interesting Study",
            "doi": "10.039f/spe39",
            "type": "Journal Article"
        }, 
        ...
    ].
    '''
    publications = []
    for filename in filenames:
        print(f'Reading "{filename}"... ', end='')
        try:
            with open(filename, encoding='utf-8') as f:
                pubs = json.load(f)
                publications += pubs
            print(f'Success! ({len(pubs)})')
        except FileNotFoundError:
            print(f'Not found')
        except IOError:
            print(f'Read error')
    return publications

def write_pubs(publications: list, filename: str):
    try:
        with open(filename, 'w') as f:
            json.dump(publications, f, indent=4)
    except:
        print('A write error occurred')

def main(argv: list):
    dois_only = False
    outputfile = default_outputfile
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ofile="])
    except getopt.GetoptError:
        print('collect.py -o <outputfile> [dois]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('collect.py -o <outputfile> [dois]')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if 'dois' in argv:
        print('dois only')
        dois_only = True
    publications = read_pubs(filenames)
    if dois_only == True:
        items = [pub.get('doi', '').strip() for pub in publications if 'doi' in pub and pub['doi'].strip() != '']
    else:
        items = publications
    item_type = 'DOIs' if dois_only == True else 'publications'
    print(f' > Imported {len(items)} {item_type}.\n')
    write_pubs(items, outputfile)
    print(f' > Successfully wrote to {outputfile}.\n')

###

json_path = '../library'
filenames = [f'{json_path}/{i}.json' for i in range(2005, 2019)]
default_outputfile = './library.json'

if __name__ == "__main__":
    print()
    main(sys.argv[1:])