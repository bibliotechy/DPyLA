import unittest
from dpla.api import *
import os

class testDPyLAClass(unittest.TestCase):


    def test_api_key_passed_as_parameter(self):
        key = "YourDPLAApiKeyGoesHereShouldBe32"
        dpla = DPLA(key)
        message = "Valid key passed as param should be set as attribute"
        self.assertEqual(dpla.api_key, key, message)


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
        self.query              = self.r._singleValueFormatter('q','chicken')
        self.multiword_query    = self.r._singleValueFormatter('q','chicken man')
        self.multivalue_fields  = self.r._multiValueFormatter('fields',["sourceResource.title", "sourceResource.spatial.state"])
        self.search_fields      = self.r._searchFieldsFormatter({"sourceResource.title" : "Chicago", "sourceResource.subject" : "Food"})

    def test_single_value_formatter(self):
        expected = "q=chicken"
        self.assertEqual(self.query, expected, 'Single word single values are formattted correctly')
        expected = "q=chicken+man"
        self.assertEqual(self.multiword_query, expected, 'Multi word single values are formattted correctly')

    def test_multivalue_fields_formatter(self):
        expected = "fields=sourceResource.title%2CsourceResource.spatial.state"
        self.assertEqual(self.multivalue_fields, expected, "Return fields url fragment are correct")

    def test_search_field_formatter(self):
        expected = ("sourceResource.title=Chicago", "sourceResource.subject=Food")
        for expect in expected:
            self.assertIn(expect, self.search_fields, "Search specific fields url fragments are correct")

    def test_spatial_facet_formatter(self):
        request  = self.r._facetSpatialFormatter([37, -48])
        expected = "facets=sourceResource.spatial.coordinates%3A37%3A-48"
        self.assertEqual(request, expected, "Spatial facets url fragments are correct")

    def test_build_url(self):
        url_parts = []

        url_parts.append(self.query)
        expected = "https://api.dp.la/v2/items?q=chicken&api_key="
        url = self.r._buildUrl("items", url_parts)

        self.assertEqual(url, expected, "Single parameter item search url is constructed correctly")

        url_parts.append(self.multivalue_fields)
        url = self.r._buildUrl("items", url_parts)
        expected = "https://api.dp.la/v2/items?q=chicken&fields=sourceResource.title%2CsourceResource.spatial.state&api_key="
        self.assertEqual(url, expected, "Two parameter item search url is constructed correctly")

        url_parts.append(self.search_fields)
        url = self.r._buildUrl("items", url_parts)

        expected = (
            'q=chicken', 'sourceResource.title=Chicago', 'sourceResource.subject=Food', 'api_key=',
            'fields=sourceResource.title%2CsourceResource.spatial.state'
        )
        for expect in expected:
            self.assertIn(expect, url, "Three parameter item search url is constructed correctly")

        id = "93583acc6425f8172b7b506f44a32121"
        url = self.r._buildUrl("items", id=id)
        expected = "https://api.dp.la/v2/items/93583acc6425f8172b7b506f44a32121?api_key="
        self.assertEqual(url, expected)

        multiple_ids = "fe47a8b71de4c136fe115a19ead13e4d,93583acc6425f8172b7b506f44a32121"
        url = self.r._buildUrl("items", id=multiple_ids)
        expected = "https://api.dp.la/v2/items/fe47a8b71de4c136fe115a19ead13e4d,93583acc6425f8172b7b506f44a32121?api_key="
        self.assertEqual(url, expected)


class DPyLASearch(unittest.TestCase):

    def setUp(self):
      api_key = os.environ['DPLA_API_KEY']
      self.dpla = DPLA(api_key)

    def test_search_simple(self):
      results = self.dpla.search("chickens")
      self.assertGreaterEqual(results.count, 0, "Results count should contain at least one result")

class DPyLAResults(unittest.TestCase):

    def setUp(self):
      api_key = os.environ['DPLA_API_KEY']
      self.dpla = DPLA(api_key)

    def test_all_records_method(self):
        results = self.dpla.search("chicken man new old", fields=["sourceResource.title"])
        count = 0
        for i in results.all_records():
            count += 1
        self.assertEqual(results.count, count,
                         "Iterates through %i records, but %i are in result" % (count, results.count))


if __name__ == '__main__':
    unittest.main()
