# RENCI Publications

## What is This?

This repo houses publication information for RENCI.
For archival purposes, the steps on how the past publication information was harvested is detailed below.

### Steps to Gather Past Publication Information

#### Harvest Citations from SharePoint

Current citations live inside `div`s with id `tabYYYY-slug`, where `YYYY` is the year the publications were published. These are the IDs assigned by the WordPress plugin used on that page.

Scrape the page with Javascript, with something like the following.

```javascript
const num = 10
publications = []
for (let i = 2005; i <= 2018; i++) {
    const idValue = 2020 - i
    const titleID = `#titl${ num }-${ idValue }_`
    const bodyID = `#tbod${ num }-${ idValue }__`
    const year = document.querySelector(titleID).querySelector('#group0').innerText.match(/Year : (\d{4})/)[1]
    publications[year] = []
    const body = document.querySelector(bodyID).nextElementSibling
    const entries = body.querySelectorAll('.ms-itmhover')
    entries.forEach(row => {
        title = row.querySelector('.ms-vb').innerText
        type = row.querySelector('.ms-vb2').innerText
        citation = row.querySelector('.ms-rtestate-field').innerText
        const publication = { title: title, type: type, citation: citation, }
        publications[year].push(publication)
    })
}
console.log(publications)
```

\* Note that the value of `num` appears in the element id names `#titlXX-` and `#tbodXX-` this value changes on page refreshes, so be sure to inspect the element containing the date on the page for that value, and assign `num` accordinly. Executing the code will dump out an array of publications, grouped by year, to the console, like the following.

```javascript
2005: (3) [{…}, {…}, {…}]
2006: (10) [{…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}]
2007: (34) [{…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}]
...
2018: (38) [{…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}]
```

#### Harvest Citations from Website

This page only contains citations, so only an array (years) of arrays (publications) is returned.

```javascript
years = [...Array(13).keys()].map(i => i + 2006)

allCitations = []

years.map( year => {
    thisYearsCitations = []
    page = document.querySelector(`#tab${ year }-slug`)
    page.querySelectorAll('p').forEach( pub => {
        let text = pub.innerText
        if (text.trim() !== '') {
            thisYearsCitations.push(pub.innerText)
        }
      })
    allCitations[year] = thisYearsCitations
})

console.log(allCitations)
```

#### Search.crossref.org

Find publications on Crossref.org and obtain DOIs for all publications for which DOIs exist. For those not possessing a DOI, follow-up steps are to be determined.

The `./publications` directory contains lists of all harvested citations and DOIs as they are gathered manually. 

#### Building the Library

The `./utils` directory contains one helpful scripts that will combine all the publication metadata from separate JSON files into one super JSON file.

```bash
$ python collect.py [-o <outputfilename>] [dois]
```

Use the `-o` flag to specify an output file, and use the `dois` flag to indicate that only a list of DOIs should be output. Otherwise, all publication metadata will be written to file.

