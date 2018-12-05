import re

def scrape_file(filename):
    '''
    Scrape a single file for lines that look like '- TYPE: Journal Article'
    '''
    dois = []
    type_regex = '- TYPE: (.+)$'
    with open(filename) as f:
        types = []
        type_lines = [line.strip() for line in f.readlines() if '- TYPE:' in line]
        for line in type_lines:
            pub_type = re.match(type_regex, line)
            if pub_type:
                types.append(pub_type.groups()[0])
        return types
    return None

def scrape_files(filenames):
    '''
    Call DOI scraper on a list of filenames
    '''
    types = []
    for filename in filenames:
        print(f'Scraping "{ filename }"...')
        types += scrape_file(filename)
    types = list(set(types))
    print(f'> Found { len(dois) } types.')
    return types

def collect_types(types):
    counts = {}
    for t in types:
        if t in counts:
            counts[t] += 1
        else:
            counts[t] = 1
    return counts
