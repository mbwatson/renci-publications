from library import Publication, Library
from scrape import scrape_files, write_dois
from pprint import pprint

#

DOI_FILE = '../library/dois.json'
PUBLICATIONS_FILE = '../library/library.json'
DOI_FILES = [f'../library/{i}.md' for i in range(2005, 2019)]

#

# Scrape each filename for DOIs
dois = scrape_files(DOI_FILES) # Get all
# dois = scrape_files(DOI_FILES)[:3] # Get first three--small for debugging.
# Write DOI list to output file
write_dois(DOI_FILE, dois)

library = Library()
library.build(DOI_FILE)
library.write(PUBLICATIONS_FILE)