import requests
import json
from datetime import datetime

class KiwoomQuote:
    """
    키움증권 REST API의 시세(Quote) 관련 요청을 담당하는 클래스
    """
    def __init__(self, auth_handler):
        """
        KiwoomQuote 클래스 초기화.
        - auth_handler: KiwoomAuth 클래스의 인스턴스. 인증 정보를 공유합니다.
        """
        self.auth = auth_handler
        self.BASE_URL = self.auth.BASE_URL
        print("✅ 시세 조회 모듈 초기화 완료.")

    def _send_request(self, api_id: str, url_path: str, body: dict):
        """
        공통 요청 전송 함수
        """
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
                print(f"❌ API 조회 실패 ({api_id}): {data.get('return_msg')}")
                return None
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API 요청 실패 ({api_id}): {e}")
            return None

    def get_current_price(self, stock_codes: list):
        """
        하나 이상의 종목에 대한 현재가 및 주요 정보를 조회합니다. (API ID: ka10095)
        """
        print(f"🚀 현재가 조회 요청: {stock_codes}")
        api_id = "ka10095"
        url_path = "/api/dostk/stkinfo"
        codes_str = "|".join(stock_codes)
        body = {"stk_cd": codes_str}
        
        response_data = self._send_request(api_id, url_path, body)
        
        if response_data:
            return response_data.get('atn_stk_infr', [])
        return None

    def get_daily_chart(self, stock_code: str, date: str = None, adjusted_price: bool = True):
        """
        일봉 데이터를 조회합니다. (API ID: ka10081)
        """
        print(f"🚀 일봉 데이터 조회 요청: {stock_code}")
        api_id = "ka10081"
        url_path = "/api/dostk/chart"
        if date is None:
            date = datetime.now().strftime("%Y%m%d")
            
        body = {
            "stk_cd": stock_code,
            "base_dt": date,
            "upd_stkpc_tp": "1" if adjusted_price else "0"
        }
        
        response_data = self._send_request(api_id, url_path, body)
        
        if response_data:
            return response_data.get('stk_dt_pole_chart_qry', [])
        return None

    def get_after_hours_rank(self, target_rate: float = 10.0):
        """
        시간외 단일가 등락률 순위를 조회하여 기준 등락률 이상인 종목 리스트를 반환합니다.
        (API ID: ka10098)
        """
        print(f"🚀 시간외 {target_rate}% 이상 상승 종목 스캔 요청...")
        api_id = "ka10098"
        url_path = "/api/dostk/rkinfo"
        body = {"mrkt_tp": "000", "sort_base": "1", "stk_cnd": "0", "trde_qty_cnd": "0", "crd_cnd": "0", "trde_prica": "0"}
        
        response_data = self._send_request(api_id, url_path, body)
        
        if not response_data:
            return []

        # 기준 등락률(target_rate) 이상인 종목만 필터링
        found_stocks = [
            {"code": stock.get("stk_cd"), "name": stock.get("stk_nm")}
            for stock in response_data.get("ovt_sigpric_flu_rt_rank", [])
            if float(stock.get("flu_rt", 0.0)) >= target_rate
        ]
        return found_stocks