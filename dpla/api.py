from re import match
from past.builtins import xrange
from requests import get, post
from requests.compat import urlencode
from dpla import settings


class DPLA():

    def __init__(self,api_key=None):

        if api_key is not None:
            self.api_key = api_key
        else:
            raise ValueError('DPLA API requires an api key.')
        if len(self.api_key) is not 32:
            raise ValueError("The DPLA key is not in the required format. PLease check it again")

    @staticmethod
    def new_key(email_address):
        if not match(r"[^@]+@[^@]+\.[^@]+", email_address):
            print("Hmmm...That doesn't look like an email address. Please check")
            return
        else:
            r = post("http://api.dp.la/v2/api_key/" + email_address)
            if r.status_code == 201:
                print(r.content)
            else:
                print("Hmmm...there seems to have been an error.")

    def fetch_by_id(self, id=[], **kwargs):
        if not id:
            raise ValueError("No id provided to fetch")
        kwargs['id'] = id
        kwargs['key'] = self.api_key
        request = Request(**kwargs)
        return Results(get(request.url).json(), request)

    def search(self, q=None, search_type="items", **kwargs):
        """
        Builds and performs an item search.

        query -- a simple search query. Boolean Search operators allowed.
        type  -- determines what type of search to perform, items or collections
        **kwargs -- The DPLA API has many possible parameters that can be passed.
        Pass parameters as kwarg key=value pairs. Some options include:
         search in specific fields -- key = searchFields , value = dictionary of fieldname(s) and search values
          Value is searched for only in the specified field.
          Multiple fields / search terms can be listed
          List of available fields is at http://dp.la/info/developers/codex/responses/field-reference/
         return fields -- "fields" as key, list of field names as value
          Only the values of specified fields will be returned.
          If no fields are passed, values for all fields will be returned.
         facets -- 'facets' as they key, list of field names as value
          Returns a list of the most common values for that field
         spatial facet -- key = "facet_spatial" 2 item list consisting of of Lat , Long.
          Will return list of common distances from that geo-coordinate.
         facet limit -- "facet_limit" as key, number as value
          Number of facets to display (for each field?)
         sort -- "sort" as key , list of fieldnames as value.
          Results are sorted by these fields
         spatial sort -- "spatial_sort" as key, 2 item list consisting of of Lat , Long. as value
          Sort by distance from an geo-coordinate

        """
        if not q and not kwargs:
            raise ValueError("You have not entered any search criteria")
        if not search_type:
            raise ValueError("Search type must be items or collections")
        kwargs['search_type'] = search_type
        if q:
            kwargs['query'] = q
        kwargs['key'] = self.api_key

        request = Request(**kwargs)
        return Results(get(request.url).json(), request, self)

class Request():
    def __init__(self, search_type="items", **kwargs):
        self.params = kwargs
        # Build individual url fragments for different search criteria
        url_parts = []
        self.base_url = "http://api.dp.la/v2/"
        self.api_key  =  kwargs.get('key', "")
        if kwargs.get('id'):
            iid = (",".join(kwargs['id']))
        else:
            iid = ""
        if kwargs.get('query'):
            url_parts.append(self._singleValueFormatter('q',kwargs['query']))
        if kwargs.get('searchFields'):
            url_parts.append(self._searchFieldsFormatter(kwargs['searchFields']))
        if kwargs.get('fields'):
            url_parts.append(self._multiValueFormatter('fields',kwargs['fields']))
        if kwargs.get('facets') and not kwargs.get('spatial_facet'):
            url_parts.append(self._multiValueFormatter('facets',kwargs['facets']))
        if kwargs.get('spatial_facet'):
            url_parts.append(self._facetSpatialFormatter(kwargs['spatial_facet']))
        if kwargs.get('facet_size'):
            url_parts.append(self._singleValueFormatter('facet_size',kwargs['facet_size']))
        if kwargs.get('sort') and not kwargs.get('spatial_sort'):
            url_parts.append(self._singleValueFormatter('sort_by', kwargs['sort']))
        if kwargs.get('spatial_sort'):
            url_parts.append(self._singleValueFormatter('sort_by_pin', "{},{}".format(*kwargs['spatial_sort'])))
            url_parts.append(self._singleValueFormatter('sort_by', "sourceResource.spatial.coordinates"))
        if kwargs.get('page_size'):
            url_parts.append(self._singleValueFormatter('page_size',kwargs['page_size']))
        if kwargs.get('page'):
            url_parts.append(self._singleValueFormatter('page',kwargs['page']))
        # Now string all the chunks together
        self.url = self._buildUrl(search_type, url_parts, iid)

    def _singleValueFormatter(self, param_name, value):
        """
        Creates an encoded URL fragment for parameters that contain only a single value

        """
        return urlencode({param_name: value})

    def _multiValueFormatter(self, param_name, values):
        """
        Creates an encoded URL fragment for parameters that may contain multiple values.

        """
        return urlencode({param_name: ','.join(values)})

    def _searchFieldsFormatter(self, searchFields):
        """
        Creates an encoded URL fragment for searching for a value within a specific field.
        If multiple fields are specified, a single string is returned

        """
        sf = [urlencode({k:v}) for k,v in searchFields.items() if k in settings.searchable_fields]
        return '&'.join(sf)

    def _facetSpatialFormatter(self, spatial_facet):
        coords = "sourceResource.spatial.coordinates:{}:{}".format(*spatial_facet)
        return urlencode({"facets": coords})

    def _buildUrl(self, search_type, url_parts=[], id=None):
        url = self.base_url + search_type
        if id:
            url += "/" + id + "?"
        else:
            url += "?"
        if search_type == "items":
            url += "&".join(url_parts)
        if url_parts:
            url += "&api_key=" + self.api_key
        else:
            url += "api_key=" + self.api_key
        return url


class Results:
    def __init__(self, response, request, dplaObject):
        self.dpla = dplaObject
        self.request = request
        self.count = response.get('count', None)
        self.limit = response.get('limit', None)
        self.start  = response.get('start', None)
        self.items= [doc for doc in response['docs']]
        if response.get('facets', None):
            self.facets = [{k: v} for k, v in response['facets'].iteritems()]

    def next_page(self):
        params = self.request.params
        params['page'] = (self.start / self.limit) + 2
        next_response = self.dpla.search(**params)
        self.start = next_response.start
        self.items = next_response.items

    def all_records(self):
        for i in xrange(self.count):
            yield self.items[i - self.start]
            if not i < self.start + self.limit - 1:
                self.next_page()




