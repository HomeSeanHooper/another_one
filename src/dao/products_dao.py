import json
from typing import Union, List, Dict

import pandas as pd

import dao.names as names


class ProductsDAO:
    """
    We will use pandas as a database. Another option would be to use MongoMock to
    bring this solution closer to a production model
    """

    def __init__(self, data_objects: List[Dict]):
        self.data = pd.DataFrame(data_objects)
        self.data[names.PRICE] = pd.to_numeric(self.data[names.PRICE], errors='coerce')
        self.data = self.data.sort_values(by=names.PRICE)

    def get_product_by_id(self, id: str) -> Union[str, None]:
        item_row = self.data[self.data[names.ID] == id]
        if len(item_row) == 0:
            return None
        return item_row.to_dict('records')[0]

    def get_n_cheapest_products(self, n: int) -> str:
        rows = self.data.iloc[0:n]
        rows = rows.dropna(subset=[names.PRICE])
        return rows.to_dict('records')
