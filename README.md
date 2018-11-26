# RECNI Publications

## What is This?

This repo houses publication information for RENCI.
For archival purposes, the steps on how the past publication information was harvested is detailed below.

### Steps to Gather Past Publication Information

#### Harvest Citations from Current Website

Current citations live inside `div`s with id `tabYYYY-slug`, where `YYYY` is the year the publications were published. These are the IDs assigned by the WordPress plugin used on that page.

Scrape the page with Javascript, with something like the following.

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

`publications.md` is a list of all harvested citations and DOIs as they are gathered. `dois.txt` contains a list of only DOIs. This will be the master list for the next step.

#### Fetch Publication Metadata

Run DOI list through a Python script to fetch the metadata for known DOIs from the Crossref API. Store -- probably as JSON.