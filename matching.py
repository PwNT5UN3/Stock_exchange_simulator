import orderbook
import global_dicts

def fill_buy(book: orderbook.OrderBook, fill_book: orderbook.OrderBook, order: orderbook.Order, price: int):
	for key in sorted(fill_book.get_book_keys()):
		if order['qty'] > 0:
			if price >= key:
				RestingOrders = fill_book.get_price_level(key)
				for RestingOrder in RestingOrders:
					if order['qty'] <= 0:
						break
					filled_shares = min(order['qty'], RestingOrder['qty'])
					global_dicts.all_traders[RestingOrder['trader_id']].tied_shares[RestingOrder['ticker']] -= filled_shares
					global_dicts.all_traders[order['trader_id']].positions[order['ticker']] += filled_shares
					order['qty'] -= filled_shares
					RestingOrder['qty'] -= filled_shares
					trade_cost = filled_shares * key
					global_dicts.all_traders[order['trader_id']].money -= trade_cost
					global_dicts.all_traders[RestingOrder['trader_id']].money += trade_cost
			else:
				break
	if (order['qty'] > 0):
		book.add_order(price=price, order=order)
	book.clean_book()
	fill_book.clean_book()

def fill_sell(book: orderbook.OrderBook, fill_book: orderbook.OrderBook, order: orderbook.Order, price: int):
	for key in sorted(fill_book.get_book_keys(), reverse=True):
		if order['qty'] > 0:
			if price <= key:
				RestingOrders = fill_book.get_price_level(key)
				for RestingOrder in RestingOrders:
					if order['qty'] <= 0:
						break
					filled_shares = min(order['qty'], RestingOrder['qty'])
					global_dicts.all_traders[RestingOrder['trader_id']].positions[RestingOrder['ticker']] += filled_shares
					global_dicts.all_traders[order['trader_id']].tied_shares[order['ticker']] -= filled_shares
					order['qty'] -= filled_shares
					RestingOrder['qty'] -= filled_shares
					trade_cost = filled_shares * key
					global_dicts.all_traders[order['trader_id']].money += trade_cost
					global_dicts.all_traders[RestingOrder['trader_id']].money -= trade_cost
			else:
				break
	if (order['qty'] > 0):
		book.add_order(price=price, order=order)
	book.clean_book()
	fill_book.clean_book()

def fill_order(side: str, order: orderbook.Order, price: int):
	if (price > 0 and order['qty'] > 0):
		if side == 'buy':
			fill_buy(book=global_dicts.full_book[order['ticker']]['bids'], fill_book=global_dicts.full_book[order['ticker']]['offers'], order=order, price=price)
		elif side == 'sell':
			fill_sell(book=global_dicts.full_book[order['ticker']]['offers'], fill_book=global_dicts.full_book[order['ticker']]['bids'], order=order, price=price)
	