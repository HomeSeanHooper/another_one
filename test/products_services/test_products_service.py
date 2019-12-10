import unittest

from dao.products_dao import ProductsDAO
from service import products_service
import mock
import numpy as np

SAMPLE_DATA = [
{
    "id": "a",
    "name": "bdbd",
    "brand": "sds",
    "retailer": "gg",
    "price": None,
    "in_stock": True
  },
  {
    "id": "775",
    "name": "mghm",
    "brand": "badan",
    "retailer": "remail",
    "price": 100,
    "in_stock": False
  },
  {
    "id": "dgd",
    "name": "name",
    "brand": "brand",
    "retailer": "sokemanemot",
    "price": 680.32,
    "in_stock": False
  }
]


class TestProductsService(unittest.TestCase):

    def setUp(self) -> None:
        self.app = products_service.app.test_client()

    @mock.patch("service.products_service.get_dao")
    def test_get_by_id(self, mock_dao):
        mock_dao.return_value = ProductsDAO(SAMPLE_DATA)

        response = self.app.get("/data/a")
        self.assertEqual(response.status, "200 OK")
        # pesky np.nan equality checks!
        self.assertEqual(response.json["id"], SAMPLE_DATA[0]["id"])

    @mock.patch("service.products_service.get_dao")
    def test_get_by_bad_id(self, mock_dao):
        mock_dao.return_value = ProductsDAO(SAMPLE_DATA)

        response = self.app.get("/data/not_this")
        self.assertEqual(response.status, "200 OK")
        self.assertEqual(response.json, {'result': 'nothing!'})

    @mock.patch("service.products_service.get_dao")
    def test_cheapest(self, mock_dao):
        mock_dao.return_value = ProductsDAO(SAMPLE_DATA)

        response = self.app.get("/data/cheapest/3")
        self.assertEqual(response.status, "200 OK")
        self.assertListEqual(response.json, [SAMPLE_DATA[1], SAMPLE_DATA[2]])

    def test_cheapest_bad_int(self):
        response = self.app.get("/data/cheapest/vvsd3")
        self.assertEqual(response.status, "400 BAD REQUEST")