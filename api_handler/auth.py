import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pathlib import Path

class KiwoomAuth:
    """
    키움증권 REST API 인증 및 토큰 관리를 담당하는 클래스
    .env 파일로부터 설정을 로드합니다.
    """
    def __init__(self):
        """
        [수정됨] KiwoomAuth 클래스 초기화. .env 파일의 절대 경로를 찾아 환경 변수를 로드합니다.
        """
        # 현재 파일(auth.py)의 위치를 기준으로 프로젝트 루트의 .env 파일 경로를 찾습니다.
        env_path = Path(__file__).resolve().parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        
        # os.getenv를 사용하여 환경 변수 값 읽기
        self.APP_KEY = os.getenv("KIWOOM_APP_KEY")
        self.APP_SECRET = os.getenv("KIWOOM_SECRET_KEY")
        self.BASE_URL = os.getenv("KIWOOM_BASE_URL")
        
        self.access_token = None
        self.token_expires_at = None

        if all([self.APP_KEY, self.APP_SECRET, self.BASE_URL]):
            print("✅ 인증 모듈 초기화 완료. (.env)")
        else:
            print("❌ .env 파일에서 API 키를 로드하는 데 실패했습니다. 변수명과 파일 위치를 확인하세요.")

    def _issue_token(self):
        """
        신규 접근 토큰을 발급받습니다.
        """
        url = f"{self.BASE_URL}/oauth2/token"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.APP_KEY,
            "secretkey": self.APP_SECRET
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            token_data = response.json()

            if "token" in token_data:
                self.access_token = token_data["token"]
                expires_dt_str = token_data["expires_dt"]
                expires = datetime.strptime(expires_dt_str, "%Y%m%d%H%M%S")
                self.token_expires_at = expires - timedelta(minutes=5)
                print("✅ 신규 접근 토큰 발급 성공.")
                return True
            else:
                print(f"❌ 토큰 발급 실패: {token_data.get('return_msg', '알 수 없는 오류')}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ API 요청 실패: {e}")
            return False

    def get_access_token(self):
        """
        유효한 접근 토큰을 반환합니다.
        토큰이 없거나 만료되었다면 신규 발급을 시도합니다.
        """
        if self.access_token and self.token_expires_at > datetime.now():
            print("🔁 기존 토큰을 재사용합니다.")
            return self.access_token
        
        if self._issue_token():
            return self.access_token
        else:
            return None