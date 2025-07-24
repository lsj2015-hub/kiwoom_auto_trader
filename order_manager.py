class OrderManager:
    def __init__(self, order_handler):
        self.order_handler = order_handler

    def buy_market_order(self, stock_code: str, quantity: int):
        return self.order_handler.buy_market_order(stock_code, quantity)

    def sell_market_order(self, stock_code: str, quantity: int):
        return self.order_handler.sell_market_order(stock_code, quantity)