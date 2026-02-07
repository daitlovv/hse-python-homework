from typing import List
from models.product import Product

def get_ordered_products_by_price(products: List[Product]) -> List[Product]:
    result = list(products)

    for i in range(len(result)):
        for j in range(0, len(result) - i - 1):
            if result[j].price < result[j + 1].price:
                result[j], result[j + 1] = result[j + 1], result[j]

    return result