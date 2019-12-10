import gzip
import tempfile
import unittest
from typing import List

import mock

from data.ingest import read_zipped_file, ingest_defaults


class TestIngest(unittest.TestCase):

    @staticmethod
    def write_zipped_data_in_source(data_source: str, data: List[List]) -> None:
        with gzip.open(data_source, 'wb') as _out:
            header = ', '.join(data[0]) + '\n'
            _out.write(header.encode("utf-8"))
            for item in data[1:]:
                data_values_string = ', '.join(item) + '\n'
                _out.write(data_values_string.encode('utf-8'))

    def test_read_small_gzip(self):
        data = [
            ['Id', 'b', 'Price', 'in_stock'],
            ["100", "hello world", "100", "True"],
            ["101", "hello world", "not a price", "False"],
            ["102", "hello world", "100.05", "True"],
            ["108", "hello world", "100.05", "Ooops"],
            ["103", "this data is wrong"],
            ["and so is this"]
        ]
        expected_data = [{'id': '100', 'b': 'hello world', 'price': 100.0, 'in_stock': True},
                         {'id': '101', 'b': 'hello world', 'price': None, 'in_stock': False},
                         {'id': '102', 'b': 'hello world', 'price': 100.05, 'in_stock': True},
                         {'id': '108', 'b': 'hello world', 'price': 100.05, 'in_stock': False}]
        temp_file = tempfile.NamedTemporaryFile()
        TestIngest.write_zipped_data_in_source(temp_file.name, data)
        data_objects = read_zipped_file(float_cols=['Price'], bool_cols=['in_stock'], zipped_file_name=temp_file.name)
        self.assertListEqual(data_objects, expected_data)

    @mock.patch("data.ingest.read_zipped_file")
    @mock.patch("data.ingest.read_downloaded_file")
    @mock.patch("data.ingest.boto3")
    def test_ingest_defaults(self, mock_boto, mock_downloaded, mock_zipped):
        mock_downloaded.return_value = [{'a': 1}]
        mock_zipped.return_value = [{'b': 2}]
        data_objects = ingest_defaults()
        self.assertListEqual([{'b': 2}, {'a': 1}], data_objects)
