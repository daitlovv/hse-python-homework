class Product:
    def __init__(self, name: str, category: str, price: float) -> None:
        self.name = name
        self.category = category
        self.price = price
        self.sale = 0

    def edit_category(self, new_category: str) -> None:
        self.category = new_category

    def edit_price(self, new_price: float) -> None:
        self.price = new_price

    def set_sale(self, sale: float) -> None:
        self.sale = sale

    def cancel_sale(self) -> None:
        self.sale = 0

    def get_price(self) -> float:
        if self.sale > 0:
            return self.price * (1 - self.sale / 100)
        return self.price

    def __repr__(self) -> str:
        return f"Товар '{self.name}' (категория '{self.category}', цена = {self.price}{', скидка ' + str(self.sale) + '%' if self.sale > 0 else ''})"
