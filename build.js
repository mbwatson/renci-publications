let axios = require('axios')
let fs = require('fs')

const url = (doi) => `https://search.crossref.org/citation?format=apa&doi=${doi}`
const doiFile = fs.readFileSync("./dois.txt").toString('utf-8');
const dois = doiFile.split('\n').slice(0, 5).map(doi => doi.trim())

let pubLibrary = []

const fetchLibrary = async () => {
    try {
        let publications = dois.map(doi =>
            axios(url(doi))
                .then(response => {
                    pubLibrary.push(response.data)
                    return response.data
                })
                .catch(err => err)
        )
        let library = await Promise.all(publications)
        library.forEach(publication => {
            console.log(publication)
        })
    } catch (error) {
        console.error('Error:', error)
    }
}

fetchLibrary()
console.log(pubLibrary)