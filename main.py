from matching import *
from traders import *

if __name__ == "__main__":
	market_maker = market_maker("MM", 0, "MM")
	market_maker.give_initial_positions()
	market_maker.make_initial_offers()
	test = Trader("GCM1", 500000, "GCM")
	print("--------------------------------------------------------------")
	for trader in global_dicts.all_traders.keys():
		print(f"Positions: {global_dicts.all_traders.get(trader).positions}")
		print(f"Tied shares: {global_dicts.all_traders.get(trader).tied_shares}")
		print("-_-_-_")
	print("--------------------------------------------------------------")
	for ticker in global_dicts.full_book.keys():
		global_dicts.full_book[ticker]['bids'].print_book()
	print("--------------------------------------------------------------")
	for ticker in global_dicts.full_book.keys():
		global_dicts.full_book[ticker]['offers'].print_book()
	print('--------------------------------------------------------------')
	test.submit_limit_order('PBNJ', 20, 10100, 'buy')
	for ticker in global_dicts.full_book.keys():
		global_dicts.full_book[ticker]['bids'].print_book()
	print("--------------------------------------------------------------")
	for ticker in global_dicts.full_book.keys():
		global_dicts.full_book[ticker]['offers'].print_book()
	print('--------------------------------------------------------------')
	for trader in global_dicts.all_traders.keys():
		print(f"Positions: {global_dicts.all_traders.get(trader).positions}")
		print(f"Tied shares: {global_dicts.all_traders.get(trader).tied_shares}")
		print("-_-_-_")
	print("--------------------------------------------------------------")
	print(global_dicts.all_traders['GCM1'].positions)
	print(global_dicts.all_traders['GCM1'].money)
	print(global_dicts.all_traders['GCM1'].open_orders)