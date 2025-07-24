import yaml
import argparse  # argparse 라이브러리 추가
from api_handler.auth import KiwoomAuth
from api_handler.quote import KiwoomQuote
from api_handler.order import KiwoomOrder
from utils.strategy_loader import load_strategies
from data_manager import DataManager
from order_manager import OrderManager

def run(strategy_to_run: str):
    """
    지정된 단일 전략을 실행합니다.
    """
    # 1. 설정 로드
    with open("config/strategy_config.yaml", encoding='UTF-8') as f:
        config = yaml.safe_load(f)

    # 2. 사용 가능한 모든 전략을 동적으로 로드
    available_strategies = load_strategies()
    
    # 3. 실행할 전략이 사용 가능한지 확인
    if strategy_to_run not in available_strategies:
        print(f"❌ 오류: '{strategy_to_run}' 전략을 찾을 수 없습니다.")
        print(f"사용 가능한 전략: {list(available_strategies.keys())}")
        return

    # 4. 핵심 핸들러 및 매니저 초기화
    auth = KiwoomAuth()
    quote_handler = KiwoomQuote(auth)
    order_handler = KiwoomOrder(auth)
    data_manager = DataManager(quote_handler)
    order_manager = OrderManager(order_handler)

    print(f"\\n--- '{strategy_to_run}' 전략 실행 준비 ---")
    
    # 5. 지정된 단일 전략을 실행
    strategy_class = available_strategies[strategy_to_run]
    strategy_settings = config.get(strategy_to_run, {})
    
    # 전략 인스턴스 생성
    strategy_instance = strategy_class(settings=strategy_settings)
    
    # TODO: 이 부분을 스케줄러에 등록하여 주기적으로 실행하도록 변경해야 합니다.
    # 지금은 한 번만 즉시 실행합니다.
    strategy_instance.check_signals(
        quote_handler=quote_handler,
        order_handler=order_manager,
        data_manager=data_manager
    )

if __name__ == "__main__":
    # --- 명령줄 인자 파서 설정 ---
    parser = argparse.ArgumentParser(description="키움증권 자동매매 프로그램을 실행합니다.")
    
    # 'strategy' 라는 이름의 인자를 받도록 설정
    parser.add_argument('strategy', type=str, nargs='?', default=None,
                        help='실행할 전략의 클래스 이름을 입력합니다. (예: AfterHoursStrategy)')

    args = parser.parse_args()

    if args.strategy:
        # 인자로 전략 이름이 들어온 경우, 해당 전략 실행
        run(strategy_to_run=args.strategy)
    else:
        # 인자가 없는 경우, 사용법 안내
        print("🛑 실행할 전략의 이름을 입력해야 합니다.")
        print("사용 예시: python main.py AfterHoursStrategy")
        
        # 사용 가능한 전략 목록을 보여주기 위해 임시로 로드
        print("\\n--- 사용 가능한 전략 목록 ---")
        load_strategies()