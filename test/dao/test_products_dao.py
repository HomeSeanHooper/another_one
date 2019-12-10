import json
import unittest

from dao.products_dao import ProductsDAO


class TestProductsDAO(unittest.TestCase):

    def test_get_by_index(self):
        data = [{"id": "2", "value": 4, "price": 10},
                {"id": "4", "value": 8, "price": 12},
                ]
        products_dao = ProductsDAO(data)
        result = products_dao.get_product_by_id("2")
        self.assertEqual(data[0], result)
        result = products_dao.get_product_by_id("4")
        self.assertEqual(data[1], result)

    def test_get_by_missing_index(self):
        data = [{"id": "2", "value": 4, "price": 10}
                ]
        products_dao = ProductsDAO(data)
        result = products_dao.get_product_by_id("4")
        self.assertEqual(None, result)

    def test_get_n_cheapest_products(self):
        data = [{"id": "2", "value": 4, "price": 10},
                {"id": "3", "value": 4, "price": 1},
                {"id": "7", "value": 8, "price": 0},
                ]
        products_dao = ProductsDAO(data)
        result = products_dao.get_n_cheapest_products(2)
        expected_result = [{"id": "7", "value": 8, "price": 0}, {"id": "3", "value": 4, "price": 1}]
        self.assertEqual(expected_result, result)

    def test_get_n_cheapest_products_but_no_nans(self):
        data = [
            {"id": "8", "value": 8, "price": None},
            {"id": "9", "value": 8, "price": None},
            {"id": "10", "value": 8, "price": 100},
        ]
        products_dao = ProductsDAO(data)
        result = products_dao.get_n_cheapest_products(2)
        expected_result = [{"id": "10", "value": 8, "price": 100.0}]
        self.assertEqual(expected_result, result)

    def test_get_n_cheapest_products_bad_price(self):
        data = [
            {"id": "8", "value": 8, "price": 'XXXXX'},
            {"id": "9", "value": 8, "price": None},
            {"id": "10", "value": 8, "price": 'YYYY'},
        ]
        products_dao = ProductsDAO(data)
        result = products_dao.get_n_cheapest_products(2)
        expected_result = []
        self.assertEqual(expected_result, result)