![Travis icons](https://travis-ci.org/bibliotechy/DPyLA.png)


#DPyLA - A Python client for the DPLA API
#### under active development! 

[The DPLA](http://dp.la) (Digital Public Library of America) is aggregation  digital library, archive and museum collections. What really makes it stand out is it's awesome API. This python library is a wrapper around that API, making it easier to interact with.

####Getting started


`>>> from dpla import DPLA`

The create the dpla object with your DPLA API key.

`>>> dpla = DPLA('your-key-here')`

Now, create create your first search

```

>>> result = dpla.search(q='chicken')
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
  u'format': u'Images',
  u'language': [{u'iso639_3': u'eng', u'name': u'English'}],
  u'rights': u'This digital resource may be freely searched and displayed. Permission must be received for subsequent distribution in print or electronically. Physical rights are retained by the owning repository. Copyright is retained in accordance with U. S. copyright laws. Please go to http://kdl.kyvl.org for more information.',
  u'stateLocatedIn': [{u'name': u'University of Kentucky'}],
  u'subject': [{u'name': u'Agriculture-United States'},
   {u'name': u'Animal Culture-United States'},
   {u'name': u'Photographs of animals'},
   {u'name': u'Photographs of livestock'}],
  u'title': u'Chicken',
  u'type': u'text'}}
>>> result.count # tells you how many DPLA records matched your search
925
>>> results.limit # tells you how many you actually got back.
10 #Unless you tel it otherwise, DPLA Api sets the limit to ten.


```

