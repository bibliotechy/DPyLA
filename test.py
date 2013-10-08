import unittest
from dpla import *
import settings


class testDPyLAClass(unittest.TestCase):

    def setUp(self):
        self.dpla = DPLA()

    def test_api_key_passed_as_parameter(self):
        key = "9da474273d98c8dc3dc567939e89f9f8"
        dpla = DPLA(key)
        message = "Valid key passed as param should be set as attribute"
        self.assertEqual(dpla.api_key, key, message)

    def test_api_key_from_settings(self):
        message = "Valid key in settings should be set as attribute"
        self.assertEqual(self.dpla.api_key, settings.API_KEY, message)

    def test_missing_api_key(self):
        settings.API_KEY = None
        with self.assertRaises(ValueError):
            dpla = DPLA()

    def test_invalid_api_key(self):
        with self.assertRaises(ValueError):
            dpla = DPLA("shortstring")


class DPyLARequest(unittest.TestCase):

    def setUp(self):
        self.r = Request()

    def test_sort_init(self):
        r1 = self.r
        r1._sort_init({'field' : 'sourceResource.title'})
        self.assertEqual("sort_by=sourceResource.title&", r1.sortBy)
        r1._sort_init({'spatial':  ('47','-38')})
        self.assertEqual("sort_by_pin=47%2C-38&", r1.spatialSort)
        msg = "If Spatial sort, then sortBy must be coordinates"
        self.assertEqual("sort_by=sourceResource.spatial.coordinates&", r1.sortBy, msg)

    def test_facet_init(self):
        r2 = self.r
        r2._facets_init({'fields' : ['sourceResource.title']})
        self.assertEqual("facets=sourceResource.title&", r2.facets, "Single facet url fragment correct")
        r2._facets_init({'fields' : ['sourceResource.title', 'sourceResource.spatial.city']})
        expected = "facets=sourceResource.title%2CsourceResource.spatial.city&"
        self.assertEqual(expected, r2.facets, "Multiple facet url fragment is correct")
        r2._facets_init({'fields' : 'sourceResource.title', 'limit' : '5'})
        self.assertEqual("facet_size=5&", r2.facets_limit)
        r2._facets_init({"spatial" : ['48', '-37']})
        self.assertEqual("facets=sourceResource.spatial.coordinates%3A48%3A-37&", r2.facets)

    def test_paging_init(self):
        r3 = self.r
        r3._paging_init({'page_size' : 50, 'page' : 5 })
        self.assertEqual("page_size=50&", r3.page_size, "Page size url fragment is correct")
        self.assertEqual('page=5&', r3.page, 'Page url fragment is correct')

    def test_multivalue_fields_formatter(self):
        request  = Request(returnFields=('sourceResource.title', 'sourceResource.spatial.state'))
        expected = "fields=sourceResource.title%2CsourceResource.spatial.state&"
        self.assertEqual(request.returnFields, expected, "Return fields url fragment are correct")

    def test_search_field_formatter(self):
        request = Request(searchFields=({"sourceResource.title" : "Chicago", "sourceResource.subject" : "Food"}))
        expected = "sourceResource.title=Chicago&sourceResource.subject=Food&"
        self.assertEqual(request.searchFields, expected, "Search specific fields url fragments are correct")

    def test_build_url(self):
        request = Request("chicken",searchFields=({'sourceResource.title': "Model"}))
        expected = 'http://api.dp.la/v2/items?q=chicken&sourceResource.title=Model&api_key=9da474273d98c8dc3dc567939e89f9f8'
        self.assertEqual(request.url, expected)




if __name__ == '__main__':
    unittest.main()