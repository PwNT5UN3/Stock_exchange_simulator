from typing import Dict, List, Union, TypedDict
import random
from dataclasses import dataclass

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

def	generate_order_id(trader_id: str):
	return (trader_id + "|" + str(random.getrandbits(64)))

full_book = {
    "NDYS": {"bids": OrderBook(), "offers": OrderBook(), "name": "NovaDyne Systems"},
    "HLXN": {"bids": OrderBook(), "offers": OrderBook(), "name": "Helixion Interactive"},
    "BCIC": {"bids": OrderBook(), "offers": OrderBook(), "name": "BlueCrest Infrastructure Corp."},
    "PBNJ": {"bids": OrderBook(), "offers": OrderBook(), "name": "PBNJ Foods & Consumer Brands"},
    "QHTC": {"bids": OrderBook(), "offers": OrderBook(), "name": "Quantum Harbor Technologies"},
    "SWVC": {"bids": OrderBook(), "offers": OrderBook(), "name": "StellarWave Communications"},
    "GMEG": {"bids": OrderBook(), "offers": OrderBook(), "name": "GreenMantle Energy Group"},
    "ASTR": {"bids": OrderBook(), "offers": OrderBook(), "name": "Asterion Automotive"},
    "RVFH": {"bids": OrderBook(), "offers": OrderBook(), "name": "Riverstone Financial Holdings"},
    "ALEM": {"bids": OrderBook(), "offers": OrderBook(), "name": "ArcLight Entertainment Media"}
}

@dataclass
class position:
	ticker: str
	qty: int

class Trader:
	def __init__(self, id: str, money: int, Broker: str):
		self.id = id
		self.money = money
		self.positions: List[position] = []
		self.open_orders: Dict[str, Order] = {}
		self.Broker = Broker

	def submit_limit_order(self, ticker: str, qty: int, price: int, side: str):
		order_id = generate_order_id(self.id)
		while (order_id in self.open_orders):
			order_id = generate_order_id(self.id)
		order = Order(trader_id=self.id, order_id=order_id, qty=qty, ticker=ticker, side=side)
		fill_order(side=side, order=order, price=price)
		self.open_orders[order_id] = order

	def clear_orders(self):
		for key in list(self.open_orders.keys()):
			if self.open_orders[key]['qty'] == 0:
				del self.open_orders[key]

	def print_orders(self):
		print(self.open_orders)

all_traders = {}

def fill_buy(book: OrderBook, fill_book: OrderBook, order: Order, price: int):
	for key in sorted(fill_book.get_book_keys()):
		if order['qty'] > 0:
			if price >= key:
				RestingOrders = fill_book.get_price_level(key)
				for RestingOrder in RestingOrders:
					if order['qty'] <= 0:
						break
					print(RestingOrder)
			else:
				break
	if (order['qty'] > 0):
		book.add_order(price=price, order=order)
	book.clean_book()
	fill_book.clean_book()

def fill_sell(book: OrderBook, fill_book: OrderBook, order: Order, price: int):
	for key in sorted(fill_book.get_book_keys(), reverse=True):
		if order['qty'] > 0:
			if price <= key:
				RestingOrders = fill_book.get_price_level(key)
				for RestingOrder in RestingOrders:
					if order['qty'] <= 0:
						break
					print(RestingOrder)
			else:
				break
	if (order['qty'] > 0):
		book.add_order(price=price, order=order)
	book.clean_book()
	fill_book.clean_book()

def fill_order(side: str, order: Order, price: int):
	if (price > 0 and order['qty'] > 0):
		if side == 'buy':
			fill_buy(book=full_book[order['ticker']]['bids'], fill_book=full_book[order['ticker']]['offers'], order=order, price=price)
		elif side == 'sell':
			fill_sell(book=full_book[order['ticker']]['offers'], fill_book=full_book[order['ticker']]['bids'], order=order, price=price)
	

if __name__ == "__main__":
	test = Trader("BR1", 1000, "BR")
	all_traders[test.id] = test
	i = 0
	while (i < 3):
		test.submit_limit_order("PBNJ", 100, i, 'buy')
		i += 1
	test_entry = list(test.open_orders.items())[1]
	print(test_entry)
	if (test_entry[1]['side']) == 'buy':
		for key in full_book[test_entry[1]['ticker']]['bids'].get_book_keys():
			RestingOrders = full_book[test_entry[1]['ticker']]['bids'].get_price_level(key)
			for RestingOrder in RestingOrders:
				if RestingOrder['order_id'] == test_entry[1]['order_id']:
					print(RestingOrder)
	else:
		for key in full_book[test_entry[1]['ticker']]['offers'].get_book_keys():
			RestingOrders = full_book[test_entry[1]['ticker']]['bids'].get_price_level(key)
			for RestingOrder in RestingOrders:
				if RestingOrder['order_id'] == test_entry[1]['order_id']:
					print(RestingOrder)
	for key in full_book[test_entry[1]['ticker']]['bids'].get_book_keys():
			RestingOrders = full_book[test_entry[1]['ticker']]['bids'].get_price_level(key)
			for RestingOrder in RestingOrders:
				if RestingOrder['order_id'] == test_entry[1]['order_id']:
					RestingOrder['qty'] = 0
					print(RestingOrder)
	print(test_entry)
	print("-----------------------------------------------")
	for order in test.open_orders:
		print(test.open_orders.get(order))
	test.clear_orders()
	for order in test.open_orders:
		print(test.open_orders.get(order))