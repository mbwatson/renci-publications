from library import Publication, Library
from pprint import pprint

#

FILE_IN_DOIS = '../library/dois.txt'
FILE_OUT_JSON = '../library/library.json'

#

library = Library()

library.build(FILE_IN_DOIS)
library.write(FILE_OUT_JSON)