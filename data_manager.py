class DataManager:
    def __init__(self, quote_handler):
        self.quote_handler = quote_handler
        self.portfolio = []

    def update_portfolio(self):
        # TODO: 계좌평가잔고내역요청(kt00018) API를 사용하여 실제 잔고 업데이트
        # 현재는 임시로 비워둡니다.
        print("INFO: 포트폴리오 정보를 업데이트합니다. (현재는 기능 구현 전)")
        self.portfolio = [] 

    def get_portfolio(self):
        return self.portfolio