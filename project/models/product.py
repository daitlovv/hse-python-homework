class Product:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price
        self.sale = 0

    def edit_category(self, new_category):
        self.category = new_category

    def edit_price(self, new_price):
        self.price = new_price

    def set_sale(self, sale):
        self.sale = sale

    def cancel_sale(self):
        self.sale = 0

    def get_price(self):
        if self.sale > 0:
            return self.price * (1 - self.sale / 100)
        return self.price

    def __repr__(self):
        return f"Товар '{self.name}' (категория '{self.category}', цена = {self.price}{', скидка ' + str(self.sale) + '%' if self.sale > 0 else ''})"
