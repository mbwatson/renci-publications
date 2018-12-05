import re

def scraper(filename):
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

def scrape_files_for_dois(filenames):
    '''
    Call DOI scraper on a list of filenames
    '''
    dois = []
    for filename in filenames:
        print(f'Scraping "{ filename }"...')
        dois += scraper(filename)
    dois = list(set(dois))
    print(f'> Scraped { len(dois) } DOIs.')
    return dois

def write_dois(filename, dois):
    with open(filename, 'w') as f:
        for doi in dois:
            f.write(doi + '\n')
    print(f'> Wrote { len(dois) } DOIs to { filename }.')

###

# Filenames are 2005.ms, 2006.md, ..., 2018.md
doi_files = [f'../library/{i}.md' for i in range(2005, 2019)]
# Scrape each filename for DOIs
dois = scrape_files_for_dois(doi_files)
# Write DOI list to output file
write_dois('../library/dois.txt', dois)
