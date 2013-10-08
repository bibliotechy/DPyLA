from requests import get
from requests.compat import urlencode
import settings


class DPLA():

    def __init__(self,api_key=None):

        if api_key is not None:
            self.api_key = api_key
        elif settings.API_KEY is not None:
            self.api_key = settings.API_KEY
        else:
            raise ValueError('DPLA API requires an api key. Run DPLA.get_key() to request one')
        if len(self.api_key) is not 32:
            raise ValueError("The DPLA key is in the required format. PLease check it again")

    def itemSearch(self,query=None,**kwargs):
        """
        Builds and performs an item search.

        query -- a simple search query. Boolean Search operators allowed.
        searchFields -- Dictionary  of "field name" : "search value" pairs. Value is searched for only in the specified
          field. List of available fields is at http://dp.la/info/developers/codex/responses/field-reference/
        returnFields --  Tuple of field names. Only the values of specified fields will be returned.
         If no fields are passed, values for all fields will be returned.
        facets -- Dictionary with fields, spatial & limit as valid keys.
         fields - tuple of field names,  Results will include a list of the most common values for those fields fields.
         spatial - Tuple of Lat / Long. Will return list of common distances from that geo-coordinate.
         limit - Number of facets to return (for each field?)
        sort -- Dictionary with field and spatial as valid keys.
          field -- Tuple of fields. Results are sorted by these fields
          spatial -- Lat / Long Tuple. Sort by distance from an geo-coordinate

        """

        #get the params as a dictionary

        if query:
            kwargs['query'] = query

        request = Request(**kwargs)
        return Results(get(request.url).json(), request)

class Request():
    def __init__(self, query=None, type="items", searchFields=None,returnFields=None,facets=None,sort=None,pagination=None):
        self.params = locals().pop('self')
        # Clear out object attributes
        if query:
            self.query =  self._singleValueFormatter('q',query)
        if searchFields:
            self.searchFields= self._searchFieldsFormatter(searchFields)
        if returnFields:
            self.returnFields = self._multiValueFormatter('fields',returnFields)
        if facets:
            self._facets_init(facets)
        if sort:
            self._sort_init(sort)
        if pagination:
            self._paging_init(pagination)
        self.url = self._buildUrl(type,locals())



    def _facets_init(self, facets):
        if facets.get('fields', None):
            self.facets = self._multiValueFormatter('facets',list(facets['fields']))
        if facets.get('spatial', None):
            self.facets = self._facetSpatialFormatter(facets)
        if facets.get('limit', None):
            self.facets_limit =  self._singleValueFormatter('facet_size', facets['limit'])


    def _sort_init(self, sort):
        if sort.get('field', None):
            self.sortBy = self._singleValueFormatter('sort_by', sort['field'])
        if sort.get('spatial', None):
            self.spatialSort = self._singleValueFormatter('sort_by_pin', ','.join(sort['spatial']))
            if sort.get('field', None) != "sourceResource.spatial.coordinates":
                self.sortBy = self._singleValueFormatter('sort_by', "sourceResource.spatial.coordinates")


    def _paging_init(self, pagination):
        self.pagination = ""
        if pagination.get('page_size', None):
            self.page_size = self._singleValueFormatter('page_size', pagination['page_size'])
            self.pagination += self.page_size
        if pagination.get('page', None):
            self.page = self._singleValueFormatter('page', pagination['page'])
            self.pagination += self.page



    def _singleValueFormatter(self, param_name, value):
            return urlencode({param_name: value}) + "&"

    def _searchFieldsFormatter(self, searchFields):
        sf = [urlencode({k:v}) for k,v in searchFields.items() if k in settings.searchable_fields]
        return '&'.join(sf) + "&"

    def _facetSpatialFormatter(self, facets):
        coords = "sourceResource.spatial.coordinates:{}:{}".format(*facets['spatial'])
        return urlencode({"facets": coords}) + "&"

    def _multiValueFormatter(self, param_name, values):
        return urlencode({param_name: ','.join(values)}) + "&"

    def _flushPreviousValues(self):
        for param in self.params:
            self.__dict__[param] = None

    def _buildUrl(self, type, kwargs=None):
        url = settings.BASE_URL + type + "?"
        for param in kwargs:
            if self.__dict__.get(param, None):
                url += self.__dict__[param]
        url += "api_key=" + settings.API_KEY
        self.url = url
        return url


class Results():
    def __init__(self, response, request):
        self.request = request
        self.count = response['count']
        self.limit = response['limit']
        self.start  = response['start']
        self.items= [doc for doc in response['docs']]
