![Travis icons](https://travis-ci.org/bibliotechy/DPyLA.png)


#DPyLA - A Python client for the DPLA API

[The DPLA](http://dp.la) (Digital Public Library of America) is aggregation  digital library, archive and museum collections. What really makes it stand out is it's awesome API. This python library is a wrapper around that API, making it easier to interact with.

####Getting started


`>>> from dpla import DPLA`

The create the dpla object with your DPLA API key.

`>>> dpla = DPLA('your-key-here')`

Now, create create your first search

```
>>> dpla.itemSearch('chicken')
>>> dpla.results.count
925
>>> dpla.results.items[0]

```

