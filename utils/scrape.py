import re
import json

def scrape_file(filename):
    '''
    Scrape a single file for lines that look like '- DOI: 10.1021/jp046536e'
    '''
    dois = []
    doi_regex = '- DOI: (.+\/.+)$'
    with open(filename) as f:
        dois = []
        doi_lines = [line.strip() for line in f.readlines() if '- DOI:' in line]
        for line in doi_lines:
            doi = re.match(doi_regex, line)
            if doi:
                dois.append(doi.groups()[0])
        return dois

def scrape_files(filenames):
    '''
    Call DOI scraper on a list of filenames
    '''
    dois = []
    for filename in filenames:
        print(f'Scraping "{ filename }"...')
        dois += scrape_file(filename)
    dois = list(set(dois))
    print(f'> Found { len(dois) } DOIs.')
    return dois

def write_dois(filename, dois):
    '''
    Writes library to a JSON file, <filename>.
    '''
    doisJson = []
    for doi in dois:
        doisJson.append(doi)
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(doisJson, indent=2))