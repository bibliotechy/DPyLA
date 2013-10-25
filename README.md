![Travis icons](https://travis-ci.org/bibliotechy/DPyLA.png)


#DPyLA - A Python client for the DPLA API
#### under active development! 

[The DPLA](http://dp.la) (Digital Public Library of America) is aggregation  digital library, archive and museum collections. What really makes it stand out is it's awesome API. This python library is a wrapper around that API, making it easier to interact with.

####Getting started


`>>> from dpla.api import DPLA`

The create the dpla object with your DPLA API key.

`>>> dpla = DPLA('your-key-here')` 

Now, create create your first search

`>>> result = dpla.search('chicken')`

Records returned are in result.items

```
>>> result.items[0] #gets you a multidimensional dictionary of the first result. Much omitted below for brevity.
{u'@context': {u'@vocab': u'http://purl.org/dc/terms/',
  ...
 u'@id': u'http://dp.la/api/items/bc944ed8339050bbbcf25f3838895a03',
 u'_id': u'kentucky--http://kdl.kyvl.org/catalog/xt7sf7664q86_1755_1',
 ...
 u'hasView': {u'@id': u'http://nyx.uky.edu/dips/xt7sf7664q86/data/1/016_0006_p/016_0006/016_0006.jpg'},
 ...
 u'sourceResource': {u'collection': [],
  u'creator': u'University of Kentucky',
  u'language': [{u'iso639_3': u'eng', u'name': u'English'}],
  u'stateLocatedIn': [{u'name': u'University of Kentucky'}],
  u'subject': [{u'name': u'Agriculture-United States'},
   {u'name': u'Animal Culture-United States'},
   {u'name': u'Photographs of animals'},
   {u'name': u'Photographs of livestock'}],
  u'title': u'Chicken'}}
```

You can also find out how many records were found matching that criteria
```
>>> result.count # 
925
```

But you don't have all 925 records. Unless you tell it otherwise, DPLA Api sets a limit of ten records returned. 
```
>>> results.limit 
10 # 
```


But if you want more, it is easy it's easy just:
```
>>> result = dpla.search(q="chicken", page_size=100)
>>> result.limit
100 # More records, YAY!
```

###More Options
The DPLA gives you a lot of options for tailoring your search to get back exactly what you want. DPyLA helps make creating those fine grained searches easier (easier than creating your own 250-charcter url anyway!) 

####Query
A standard keyword query that searches across all fields.
Just enter a string with your search terms. If combining with other search parameters, make sure it is the first param passed.
```
>>> result = dpla.search("chicken")
>>> result = dpla.search("chicken man")
>>> result = dpla.search("chicken", fields=["sourceResource.title"])
```

####Search within specific fields
You can search within specific fields to narrow your search. 
Pass a dictionary of key / value pairs to the `searchFields` parameter, where field names are the keys and search values are the value.
```
>>> fields = {"sourceResource.title" : "crime", "sourceResource.spatial.state" : "Illinois"}
>>> result = dpla.search(searchFields=fields)
```

####Return Fields
You can also choose what fields should be included with returned records, so you only get back what you need.
Pass a list or tuple of filed names to the `fields` parameter 
```
result = dpla.search("chicken", fields=["sourceResource.title"])
>>> result.items[0]
{u'sourceResource.title': u'Chicken'}
```

####Facets
Get back a list of the most common terms within a field for this set of results. See the [DPLA facet docs](http://dp.la/info/developers/codex/requests/#faceting) for more info
```
>>> result = dpla.search("chicken", facets=["sourceResource.subject"])
>>> result.facets[0] 
{u'sourceResource.subject.name': {u'_type': u'terms',
  u'missing': 151,
  u'other': 3043,
  u'terms': [{u'count': 88, u'term': u'Poultry'},
   {u'count': 77, u'term': u'Social Life and Customs'},
   {u'count': 64, u'term': u'Agriculture'},
   {u'count': 60, u'term': u'People'},
   {u'count': 53, u'term': u'Chickens'},
   {u'count': 51, u'term': u'Restaurants'},
   {u'count': 51, u'term': u'Ethnology'},
   {u'count': 41, u'term': u'Domestic Animals'},
   {u'count': 39, u'term': u'Customs'},
   {u'count': 32, u'term': u'Festivals'},
   ....

```
####Spatial Facet
You can also facet by distance from a set of geo=coordinates. It requires extra work in the search url, so it is a seperate parameter.
Pass a length 2 list of [lat, lng]  to the parameter spatial_facet
```
>>> result = dpla.search("chicken", spatial_facet=[37,-48])
>>> result.facets[0]
{u'sourceResource.spatial.coordinates': {u'_type': u'geo_distance',
  u'ranges': [{u'from': 1200.0,
    u'max': 1296.205781266114,
    u'mean': 1277.6015482976388,
    u'min': 1265.9189942665018,
    u'to': 1300.0,
    u'total': 6388.007741488194,
    u'total_count': 5},
    ...
    ]}
```
###Facet Size
Normally, asking for facets will return A LOT OF FACETS!. If you only want a few, this is for you.
Pass a int to the paramters facet_size.
```
>>> result = dpla.search("chicken", facets=["sourceResource.subject"], facet_size=2)
>>> result.facets[1]
{u'sourceResource.subject.name': {u'_type': u'terms',
  u'missing': 151,
  u'other': 4097,
  u'terms': [{u'count': 69, u'term': u'Poultry'},
   {u'count': 47, u'term': u'Social Life and Customs'}],
  u'total': 4213}}
```

####Sort
How do you want the records sorted. Pass a string field name to the sort parameter
```
result = dpla.search("chicken", sort="sourceResource.title")
```
####Spatial Sort
You can alse sort by distance from a geo-coordinate. Pass the length 2 tuple of  [lat, lng] to the `spatial_sort parameter`
```
>>> result = dpla.search("chicken", spatial_sort=[37, -48])
```
####Page size
By Defaut, only ten records are returned per request. To increase that number, pass a integer (or string integer) to page_size paramter. The upper limit is 100 per request.
```
>>> result = dpla.search(q="chicken", page_size=100)
```

####Page
If that’s not enough, you can get the next ten items incrementing the page parameter (it’s one-indexed).
```
>>> result = dpla.search(q="chicken", page_size=100, page=2)
```



##Limitations
This project is still in it's infancy. It ain't purrfect.
* Right now, the client only does items search. Collections search and individual item fetch to come eventually.
* Does not do a great job catching exceptions, so be warned!
* Test coverage is limited.

##License

GPLV2. 
See [license.txt](license.txt)
