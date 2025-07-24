from .base_strategy import BaseStrategy

class AfterHoursStrategy(BaseStrategy):
    """
    '시간외 급등주 익일 시초가 매수' 전략.
    """
    def __init__(self, settings: dict):
        super().__init__(name="시간외 급등주 익일 시초가 매수 전략")
        self.target_rate = settings.get('target_rate', 10.0)
        self.investment_amount = settings.get('investment_amount', 100000)

    def check_signals(self, quote_handler, order_handler, data_manager):
        """
        매일 장 시작 시점에 실행되어, 전일 시간외 급등 종목을 매수합니다.
        """
        print(f"\n===== '{self.name}' 실행 =====")

        # 1. 어제 시간외 급등주 리스트 조회
        high_flyers = quote_handler.get_after_hours_rank(self.target_rate)
        if not high_flyers:
            print("INFO: 분석 대상 종목이 없습니다.")
            return

        print(f"INFO: 시간외 급등 종목 발견: {[s['name'] for s in high_flyers]}")

        # 2. 현재 보유 종목 리스트 조회
        my_portfolio = data_manager.get_portfolio()
        my_stock_codes = [stock['stk_cd'] for stock in my_portfolio]
        
        # 3. 매매 조건 판단 및 주문 실행
        for stock in high_flyers:
            if stock['code'] in my_stock_codes:
                print(f"INFO: {stock['name']}({stock['code']}) - 이미 보유한 종목입니다.")
                continue

            price_info = quote_handler.get_current_price([stock['code']])
            if not price_info: continue
            
            # 부호 제거 후 숫자로 변환
            current_price = abs(int(price_info[0].get('cur_prc', 0)))

            if current_price > 0:
                quantity = self.investment_amount // current_price
                if quantity == 0:
                    print(f"WARNING: {stock['name']} - 투자금이 부족하여 1주도 매수할 수 없습니다.")
                    continue
                
                print(f"EXECUTE: {stock['name']}({stock['code']}) - {quantity}주 시장가 매수를 요청합니다.")
                # 실제 주문 실행 (주석 해제 시 실제 주문이 나갑니다)
                # order_handler.buy_market_order(stock_code=stock['code'], quantity=quantity)
            else:
                print(f"WARNING: {stock['name']} - 현재가를 가져올 수 없어 주문 수량을 계산할 수 없습니다.")