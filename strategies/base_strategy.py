from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """
    모든 매매 전략 클래스의 기반이 되는 추상 기반 클래스(ABC).
    이 클래스를 상속받는 모든 전략은 반드시 'check_signals' 메서드를 구현해야 합니다.
    """

    def __init__(self, name: str):
        """
        전략 클래스 초기화.

        Args:
            name (str): 전략의 이름 (예: "시간외 급등주 따라잡기")
        """
        self.name = name
        print(f"🧠 전략 '{self.name}'이(가) 로드되었습니다.")

    @abstractmethod
    def check_signals(self, data_manager, order_manager):
        """
        매매 신호를 확인하고 주문을 실행하는 핵심 메서드.
        이 메서드는 하위 클래스에서 반드시 재정의(override)해야 합니다.

        Args:
            data_manager: 최신 시장 및 계좌 데이터를 제공하는 DataManager 객체.
            order_manager: 주문 실행을 담당하는 OrderManager 객체.
        """
        raise NotImplementedError("check_signals 메서드는 반드시 구현되어야 합니다.")