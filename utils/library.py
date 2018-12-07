from crossref.restful import Works
works = Works()
import datetime
import requests
import json

class Publication:
    def __init__(self, doi):
        work = works.doi(doi)
        if work:
            self.doi = doi
            if 'title' in work:
                self.title = work.get('title', '')
            if 'author' in work:
                self.authors = self._authors_names(work['author'])
            self.type = work.get('type', '')
            self.container = work.get('container-title', '')
            self.date = self.dateFromYYYYMDList(work.get('created',''))
            self.citation = self.fetch_citation(self.doi)
        else:
            self.doi = doi
            self.title = ''
            self.authors = []
            self.type = ''
            self.container = ''
            self.date = ''
            self.citation = ''

    def __str__(self):
        return self.title
    
    def dateFromYYYYMDList(self, dateParts):
        try:
            yyyy, month, day = dateParts.get('date-parts', '')[0]
        except:
            return ''
        return datetime.date(year=yyyy, month=month, day=day).__str__()

    def _authors_names(self, authors_in):
        authors = []
        for author in authors_in:
            new_author_name = ''
            if 'family' in author:
                new_author_name = author.get('family')
            if 'given' in author:
                new_author_name = author.get('given') + ' ' + new_author_name
            new_author_name = new_author_name.strip()
            if new_author_name != '':
                authors.append(new_author_name)
        return authors

    def fetch_citation(self, citation_format='apa'):
        url = f'http://dx.doi.org/{self.doi}'
        headers = {
            'Accept': 'text/bibliography; style=apa',
        }
        citation = requests.get(url, headers=headers)
        citation.encoding = 'utf-8'
        return citation.text or None

class Library:
    def __init__(self):
        self.publications = []

    def _read_dois(self, filename, count = None):
        '''
        Read existing library (specified by <filename>, if it exists.
        '''
        try:
            assert type(count) is int or count == None
            with open(filename) as f:
                if count:
                    dois = json.load(f)[:count]
                else:
                    dois = json.load(f)
        except AssertionError:
            print('Error: <count> must be of type \'int\' if set.')
            return []
        return dois

    def build(self, filename):
        '''
        Read DOIs from <filename> and build list of Publications.
        '''
        dois = self._read_dois(filename)
        publications = []
        for i in range(len(dois)):
            print(f'{i + 1}. Creating publication with DOI {dois[i]}...', end='')
            pub = Publication(dois[i])
            publications.append(pub)
            print(f'...done!')
        # for pub in publications:
        #     print(pub.title)
        #     print(pub.citation)
        #     print()
        self.publications = publications

    def write(self, filename):
        '''
        Writes library to a JSON file, <filename>.
        '''
        jsonPubs = []
        for pub in self.publications:
            jsonPubs.append(pub.__dict__)
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(jsonPubs, indent=2))