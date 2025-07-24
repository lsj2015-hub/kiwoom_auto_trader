import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path

class KiwoomOrder:
    """
    키움증권 REST API의 주문(Order) 관련 요청을 담당하는 클래스
    """
    def __init__(self, auth_handler):
        """
        KiwoomOrder 클래스 초기화.
        - auth_handler: KiwoomAuth 클래스의 인스턴스. 인증 정보를 공유합니다.
        """
        self.auth = auth_handler
        self.BASE_URL = self.auth.BASE_URL
        
        # .env 파일에서 계좌번호 로드
        env_path = Path(__file__).resolve().parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        self.ACCOUNT_NUMBER = os.getenv("KIWOOM_ACCOUNT_NUMBER")
        
        if self.ACCOUNT_NUMBER:
            print("✅ 주문 처리 모듈 초기화 완료.")
        else:
            print("❌ .env 파일에서 계좌번호(KIWOOM_ACCOUNT_NUMBER)를 찾을 수 없습니다.")

    def _send_request(self, api_id: str, url_path: str, body: dict):
        """ 공통 요청 전송 함수 """
        token = self.auth.get_access_token()
        if not token:
            return None

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
            "appkey": self.auth.APP_KEY,
            "appsecret": self.auth.APP_SECRET,
            "api-id": api_id
        }
        url = f"{self.BASE_URL}{url_path}"
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            data = response.json()

            if data.get('return_code') != 0:
                print(f"❌ API 주문 실패 ({api_id}): {data.get('return_msg')}")
                return None
            
            print(f"✅ API 주문 성공 ({api_id}): {data.get('return_msg')}")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API 요청 실패 ({api_id}): {e}")
            return None

    def _place_order(self, api_id: str, stock_code: str, quantity: int, price: int = 0, trade_type: str = "00"):
        """ 내부 공통 주문 함수 """
        url_path = "/api/dostk/ordr" # 주식 주문 URL 경로 
        body = {
            "dmst_stex_tp": "KRX",
            "stk_cd": stock_code,
            "ord_qty": str(quantity),
            "ord_uv": str(price),
            "trde_tp": trade_type # 00: 지정가, 03: 시장가 
        }
        return self._send_request(api_id, url_path, body)

    def buy_limit_order(self, stock_code: str, quantity: int, price: int):
        """ 지정가 매수 주문 (API ID: kt10000) """
        return self._place_order("kt10000", stock_code, quantity, price, "00")

    def sell_limit_order(self, stock_code: str, quantity: int, price: int):
        """ 지정가 매도 주문 (API ID: kt10001) """
        return self._place_order("kt10001", stock_code, quantity, price, "00")

    def buy_market_order(self, stock_code: str, quantity: int):
        """ 시장가 매수 주문 (API ID: kt10000) """
        return self._place_order("kt10000", stock_code, quantity, 0, "03")

    def sell_market_order(self, stock_code: str, quantity: int):
        """ 시장가 매도 주문 (API ID: kt10001) """
        return self._place_order("kt10001", stock_code, quantity, 0, "03")