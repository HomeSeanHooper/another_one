import gzip
import json
from typing import Union, List, Dict

import boto3
import os

full_path = os.path.dirname(__file__)

BUCKET_NAME = "pricesearcher-code-tests"
S3_FILE_NAME = "python-software-developer/products.json"
TARGET_NAME = os.path.join(full_path, "products.json")
ZIPPED_FILE_NAME = os.path.join(full_path, "products.csv.gz")


def download_products_file(bucket_name: str = BUCKET_NAME, s3_file_name: str = S3_FILE_NAME,
                           target_name: str = TARGET_NAME) -> str:
    if not os.path.exists(target_name):
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).download_file(s3_file_name, target_name)
    return target_name


def read_downloaded_file(file_name: str, float_cols:List[str], bool_cols:List[str]) -> List[Dict]:
    float_cols = list(map(lambda x: x.lower(), float_cols))
    bool_cols = list(map(lambda x: x.lower(), bool_cols))

    with open(file_name, 'r') as _input:
        data = json.load(_input)
    data_objects = []
    for point in data:
        valid_float_cols = all(elem in point.keys() for elem in float_cols)
        valid_bool_cols = all(elem in point.keys() for elem in bool_cols)
        if not valid_bool_cols or not valid_float_cols:
            continue
        for float_col in float_cols:
            point[float_col] = _float_or_none(point[float_col])
        for bool_col in bool_cols:
            point[bool_col] = _bool_or_false(point[bool_col])
        data_objects.append(point)
    return data


def _float_or_none(list_item: str) -> Union[float, None]:
    # How do we handle missing prices? Let's set them to nulls for now
    try:
        return float(list_item)
    except (ValueError, TypeError):
        return None


def _bool_or_false(list_item: str) -> bool:
    # How do we handle missing bools? Safest option is to set them to false
    # Also, the data is full of strings such as "y", "yes" and so on.
    # Next step would be to deal with them
    return list_item == "True"


def read_zipped_file(float_cols: List[str], bool_cols:List[str], zipped_file_name: str = ZIPPED_FILE_NAME) -> List[
    Dict]:
    float_cols = list(map(lambda x: x.lower(), float_cols))
    bool_cols = list(map(lambda x: x.lower(), bool_cols))

    with gzip.open(zipped_file_name, "rb") as _input:
        header = line = _input.readline().decode("utf-8").lower()
        data_objects = []
        keys = header.strip().split(', ')
        float_col_indexes = [keys.index(float_col) for float_col in float_cols]
        bool_col_indexes = [keys.index(bool_col) for bool_col in bool_cols]
        while line:
            line = _input.readline().decode("utf-8")
            # trim and split
            items = list(map(lambda x: x.strip(), line.replace('"', '').strip().split(", ")))
            if len(items) == len(keys):
                # convert columns to floats
                for float_col_index in float_col_indexes:
                    items[float_col_index] = _float_or_none(items[float_col_index])
                # convert columns to bools
                for bool_col_index in bool_col_indexes:
                    items[bool_col_index] = _bool_or_false(items[bool_col_index])
                data_objects.append(dict(zip(keys, items)))
            # do not attempt to parse lines of wrong length - we cannot map them with any confidence

        return data_objects


def ingest_defaults() -> List[Dict]:
    """
    Ingests all default files. Reimplement for custom files
    """
    downloaded_file = download_products_file()
    data_objects = read_zipped_file(float_cols=['price'], bool_cols=['instock'])
    data_objects.extend(read_downloaded_file(downloaded_file, float_cols=['price'], bool_cols=['in_stock']))

    return data_objects
