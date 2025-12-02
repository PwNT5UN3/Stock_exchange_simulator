import orderbook
import random
import matching
import global_dicts

def	generate_order_id(trader_id: str):
	return (trader_id + "|" + str(random.getrandbits(64)))

class Trader:
	def __init__(self, id: str, money: int, Broker: str):
		self.id = id
		self.money = money
		self.positions: Dict[str, int] = {}
		self.tied_shares: Dict[str, int] = {}
		self.open_orders: Dict[str, Order] = {}
		self.Broker = Broker
		global_dicts.all_traders[id] = self
		for ticker in global_dicts.full_book.keys():
			self.positions[ticker] = 0
		for ticker in global_dicts.full_book.keys():
			self.tied_shares[ticker] = 0

	def submit_limit_order(self, ticker: str, qty: int, price: int, side: str):
		order_id = generate_order_id(self.id)
		while (order_id in self.open_orders):
			order_id = generate_order_id(self.id)
		order = orderbook.Order(trader_id=self.id, order_id=order_id, qty=qty, ticker=ticker, side=side)
		if (side == 'sell'):
			self.tied_shares[ticker] += qty
			self.positions[ticker] -= qty
		matching.fill_order(side=side, order=order, price=price)
		self.open_orders[order_id] = order

	def clear_orders(self):
		for key in list(self.open_orders.keys()):
			if self.open_orders[key]['qty'] == 0:
				del self.open_orders[key]

	def print_orders(self):
		print(self.open_orders)

class market_maker(Trader):
	def give_initial_positions(self):
		for ticker in global_dicts.full_book.keys():
			self.positions[ticker] = global_dicts.full_book[ticker]['share_num']
	
	def make_initial_offers(self):
		for share in self.positions.keys():
			self.submit_limit_order(ticker=share, qty=self.positions.get(share), price=global_dicts.full_book[share]['initial_share_price'], side='sell')
