from typing import Dict, List, Union, TypedDict

class Order(TypedDict):
	id: str
	ticker: str
	qty: int

class OrderBook:
	def __init__(self):
		self.book: Dict[int, List[Order]] = {}
	
	def add_order(self, price: int, order: Order):
		if price not in self.book:
			self.book[price] = []
		self.book[price].append(order)
	
	def clean_book(self):
		for orders in self.book:
			if self.book[orders].qty == 0:
				del self.book[orders]

class position:
	ticker: str
	qty: int

class Trader:
	id: str
	money: int
	positions: List[position]

BidOrderBook = OrderBook()
OfferOrderBook = OrderBook()

if __name__ == "__main__":
	order = Order(id="A1", ticker="PBNJ", qty=200)
	BidOrderBook.add_order(price=10, order=order)
	print(BidOrderBook)