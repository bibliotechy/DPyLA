import unittest
from connection import *
import settings
import pprint


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
        self.assertEqual(self.dpla.api_key, settings.api_key, message)

    def test_missing_api_key(self):
        settings.api_key = None
        with self.assertRaises(ValueError):
            dpla = DPLA()

    def test_invalid_api_key(self):
        with self.assertRaises(ValueError):
            dpla = DPLA("shortstring")

    def test_item_search_init_query(self):
        dpla = DPLA()
        dpla.itemSearch("dogs")
        self.assertEqual(dpla.request.query, 'q=dogs&', "Query parameter set as attribute correctly")
        dpla.itemSearch("many dogs running")
        self.assertEqual(dpla.request.query, "q=many+dogs+running&", "Multi word query is set correctly")

    def test_item_search_init_searchFields(self):
        dpla = DPLA()
        dpla.itemSearch(searchFields={"sourceResource.title": "Chicken"})
        expected = "sourceResource.title=Chicken&"
        self.assertEqual(dpla.request.searchFields, expected, "Single Search field set correctly")
        multi = {
            "sourceResource.spatial.state" :"Illinois",
            "sourceResource.spatial.county": "Cook County"
        }
        dpla.itemSearch(searchFields=multi)
        expected = "sourceResource.spatial.state=Illinois&sourceResource.spatial.county=Cook+County&"
        self.assertEqual(dpla.request.searchFields, expected, "Multivalue searchField params sets correctly")

class DPyLA_unit(unittest.TestCase):

    def test_return_fields_formatter(self):
        request  = Request(returnFields=('sourceResource.title', 'sourceResource.spatial.state'))
        expected = "fields=sourceResource.title%2CsourceResource.spatial.state&"
        self.assertEqual(request.returnFields, expected, "Return fields url fragment are correct")



if __name__ == '__main__':
    unittest.main()