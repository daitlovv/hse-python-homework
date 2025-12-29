def select_products_by_category(products, category):
    return [product for product in products if product.category == category]
