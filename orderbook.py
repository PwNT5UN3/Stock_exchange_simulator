from typing import Dict, List, Union, TypedDict

class Order(TypedDict):
	trader_id: str
	order_id: str
	ticker: str
	qty: int
	side: str

class OrderBook:
	def __init__(self):
		self.book: Dict[int, List[Order]] = {}

	def add_order(self, price: int, order: Order):
		if price not in self.book:
			self.book[price] = []
		self.book[price].append(order)

	def clean_book(self):
		self.book = {
			price: [order for order in orders if order['qty'] > 0]
			for price, orders in self.book.items()
			if any(order['qty'] > 0 for order in orders)
		}

	def get_book_keys(self):
		return self.book.keys()
	
	def get_price_level(self, price: int):
		return self.book[price]

	# debugging tool mostly
	def print_book(self):
		for orders in sorted(self.book.keys()):
			print(f"{orders} : {self.book.get(orders)}")
