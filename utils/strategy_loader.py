# /utils/strategy_loader.py

import importlib
import inspect
import os
from pathlib import Path
from strategies.base_strategy import BaseStrategy

def load_strategies():
    """
    'strategies' 폴더를 스캔하여 BaseStrategy를 상속받는 모든 전략 클래스를
    동적으로 찾아내고 딕셔너리로 반환합니다.
    """
    strategies = {}
    strategies_dir = Path(__file__).resolve().parent.parent / 'strategies'
    
    for filename in os.listdir(strategies_dir):
        # 파이썬 파일이면서, base_strategy나 __init__가 아닌 경우에만 처리
        if filename.endswith(".py") and not filename.startswith(("__", "base_")):
            module_name = f"strategies.{filename[:-3]}"
            
            try:
                # 모듈을 동적으로 임포트
                module = importlib.import_module(module_name)
                
                # 모듈 내의 모든 클래스를 검사
                for name, cls in inspect.getmembers(module, inspect.isclass):
                    # BaseStrategy의 하위 클래스인지, 그리고 BaseStrategy 자체가 아닌지 확인
                    if issubclass(cls, BaseStrategy) and cls is not BaseStrategy:
                        # 전략 이름(클래스 이름)을 키로, 클래스 객체를 값으로 저장
                        strategies[cls.__name__] = cls
                        print(f"✅ 전략 발견: {cls.__name__}")
            except ImportError as e:
                print(f"❌ '{module_name}' 모듈 로드 실패: {e}")

    return strategies