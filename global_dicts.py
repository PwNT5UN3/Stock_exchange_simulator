import orderbook

all_traders = {}


full_book = {
    "NDYS": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "NovaDyne Systems", "share_num": 1000000, "initial_share_price": 17054},
    "HLXN": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "Helixion Interactive", "share_num": 100000, "initial_share_price": 1076},
    "BCIC": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "BlueCrest Infrastructure Corp.", "share_num": 50000, "initial_share_price": 4539},
    "PBNJ": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "PBNJ Foods & Consumer Brands", "share_num": 200000, "initial_share_price": 10022},
    "QHTC": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "Quantum Harbor Technologies", "share_num": 600000, "initial_share_price": 4567},
    "SWVC": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "StellarWave Communications", "share_num": 2000000, "initial_share_price": 34564},
    "GMEG": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "GreenMantle Energy Group", "share_num": 150000, "initial_share_price": 4235},
    "ASTR": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "Asterion Automotive", "share_num": 120000, "initial_share_price": 7463},
    "RVFH": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "Riverstone Financial Holdings", "share_num": 170000, "initial_share_price": 24617},
    "ALEM": {"bids": orderbook.OrderBook(), "offers": orderbook.OrderBook(), "name": "ArcLight Entertainment Media", "share_num": 450000, "initial_share_price": 5746}
}