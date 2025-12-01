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
    "NDYS": {"bids": OrderBook(), "offers": OrderBook(), "name": "NovaDyne Systems", "share_num": 1000000, "initial_share_price": 17054},
    "HLXN": {"bids": OrderBook(), "offers": OrderBook(), "name": "Helixion Interactive", "share_num": 100000, "initial_share_price": 1076},
    "BCIC": {"bids": OrderBook(), "offers": OrderBook(), "name": "BlueCrest Infrastructure Corp.", "share_num": 50000, "initial_share_price": 4539},
    "PBNJ": {"bids": OrderBook(), "offers": OrderBook(), "name": "PBNJ Foods & Consumer Brands", "share_num": 200000, "initial_share_price": 10022},
    "QHTC": {"bids": OrderBook(), "offers": OrderBook(), "name": "Quantum Harbor Technologies", "share_num": 600000, "initial_share_price": 4567},
    "SWVC": {"bids": OrderBook(), "offers": OrderBook(), "name": "StellarWave Communications", "share_num": 2000000, "initial_share_price": 34564},
    "GMEG": {"bids": OrderBook(), "offers": OrderBook(), "name": "GreenMantle Energy Group", "share_num": 150000, "initial_share_price": 4235},
    "ASTR": {"bids": OrderBook(), "offers": OrderBook(), "name": "Asterion Automotive", "share_num": 120000, "initial_share_price": 7463},
    "RVFH": {"bids": OrderBook(), "offers": OrderBook(), "name": "Riverstone Financial Holdings", "share_num": 170000, "initial_share_price": 24617},
    "ALEM": {"bids": OrderBook(), "offers": OrderBook(), "name": "ArcLight Entertainment Media", "share_num": 450000, "initial_share_price": 5746}
}

@dataclass
class position:
	ticker: str
	qty: int

class Trader:
	def __init__(self, id: str, money: int, Broker: str):
		self.id = id
		self.money = money
		self.positions: Dict[str, int] = {}
		self.open_orders: Dict[str, Order] = {}
		self.Broker = Broker
		all_traders[id] = self
		for ticker in full_book.keys():
			self.positions[ticker] = 0

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

class market_maker(Trader):
	def give_initial_positions(self):
		for ticker in full_book.keys():
			self.positions[ticker] = full_book[ticker]['share_num']
	
	def make_initial_offers(self):
		for share in self.positions.keys():
			self.submit_limit_order(ticker=share, qty=self.positions.get(share), price=full_book[share]['initial_share_price'], side='sell')


all_traders = {}

def fill_buy(book: OrderBook, fill_book: OrderBook, order: Order, price: int):
	for key in sorted(fill_book.get_book_keys()):
		if order['qty'] > 0:
			if price >= key:
				RestingOrders = fill_book.get_price_level(key)
				for RestingOrder in RestingOrders:
					if order['qty'] <= 0:
						break
					filled_shares = min(order['qty'], RestingOrder['qty'])
					print(f"Can fill trade for :{filled_shares}")
					all_traders[RestingOrder['trader_id']].positions[RestingOrder['ticker']] -= filled_shares
					all_traders[order['trader_id']].positions[order['ticker']] += filled_shares
					print(all_traders[RestingOrder['trader_id']].positions[RestingOrder['ticker']])
					order['qty'] -= filled_shares
					RestingOrder['qty'] -= filled_shares
					trade_cost = filled_shares * key
					print(trade_cost)
					print(all_traders[RestingOrder['trader_id']].money)
					print(all_traders[order['trader_id']].money)
					all_traders[order['trader_id']].money -= trade_cost
					all_traders[RestingOrder['trader_id']].money += trade_cost
					print(all_traders[RestingOrder['trader_id']].money)
					print(all_traders[order['trader_id']].money)
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
	market_maker = market_maker("MM", 0, "MM")
	market_maker.give_initial_positions()
	market_maker.make_initial_offers()
	test = Trader("GCM1", 500000, "GCM")
	test.submit_limit_order('PBNJ', 10, 10100, 'buy')
	for ticker in full_book.keys():
		full_book[ticker]['bids'].print_book()
	print("--------------------------------------------------------------")
	for ticker in full_book.keys():
		full_book[ticker]['offers'].print_book()
	print(all_traders)
	all_traders['MM'].print_orders()
	all_traders['GCM1'].print_orders()
	print(all_traders['GCM1'].positions)