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
		for price, orders in self.book.items():
			self.book[price] = [order for order in orders if order['qty'] > 0]
		for price in list(self.book.keys()):
			if not self.book[price]:
				del self.book[price]
	
	def get_book_keys(self):
		return self.book.keys()

	# debugging tool mostly
	def print_book(self):
		for orders in reversed(sorted(self.book.keys())):
			print(f"{orders} : {self.book.get(orders)}")

class position:
	ticker: str
	qty: int

class Trader:
	id: str
	money: int
	positions: List[position]

BidOrderBook = OrderBook()
OfferOrderBook = OrderBook()

def fill_buy(book: OrderBook, fill_book: OrderBook, order: Order, price: int):
	for key in sorted(fill_book.get_book_keys()):
		if price >= key:
			#implement buy logic
			print("buy")
		else:
			break
	if (order['qty'] > 0):
		book.add_order(price=price, order=order)
	book.clean_book()

def fill_sell(book: OrderBook, fill_book: OrderBook, order: Order, price: int):
	for key in reversed(sorted(fill_book.get_book_keys())):
		if price <= key:
			#implement sell logic
			print("sell")
		else:
			break
	if (order['qty'] > 0):
		book.add_order(price=price, order=order)
	book.clean_book()

def fill_order(side: str, order: Order, price: int):
	if side == 'buy':
		fill_buy(book=BidOrderBook, fill_book=OfferOrderBook, order=order, price=price)
	elif side == 'sell':
		fill_sell(book=OfferOrderBook, fill_book=BidOrderBook, order=order, price=price)
	

if __name__ == "__main__":
	order = Order(id="A1", ticker="PBNJ", qty=200)
	fill_order('buy', order, 100)
	order = Order(id="A2", ticker="PBNJ", qty=0)
	fill_order('buy', order, 110)
	order = Order(id="A3", ticker="PBNJ", qty=100)
	fill_order('sell', order, 90)
	order = Order(id="A4", ticker="PBNJ", qty=2100)
	fill_order('sell', order, 120)
	order = Order(id="A4", ticker="PBNJ", qty=00)
	fill_order('buy', order, 0)
	print("Bids:")
	BidOrderBook.print_book()
	print("Offers:")
	OfferOrderBook.print_book()
