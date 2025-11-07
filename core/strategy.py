from dataclasses import dataclass
from enum import Enum
import json
import os
from abc import abstractmethod, ABC
from typing import Any, TypedDict, List, Dict, Union

API = 2.0

class StrategyType(Enum):
    NONE = "NONE"
    WINWS = "WINWS"
    NFQWS = "NFQWS"

@dataclass
class StrategyWINWS:
    instructions: List[str]

@dataclass
class StrategyNFQWS:
    nft_tables: List[str]
    instructions: List[List[str]]

StrategyModelType = Union[StrategyWINWS, StrategyNFQWS]

@dataclass
class StrategiesBundle:
    type: StrategyType
    strategies: Dict[str, StrategyModelType]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StrategiesBundle':
        strategies = {}
        
        for key, strategy_data in data['strategies'].items():
            if 'nft_tables' in strategy_data:
                strategies[key] = StrategyNFQWS(
                    nft_tables=strategy_data['nft_tables'],
                    instructions=strategy_data['instructions']
                )
            else:
                strategies[key] = StrategyWINWS(
                    instructions=strategy_data['instructions']
                )
        
        return cls(
            type=StrategyType(data['type']),
            strategies=strategies
        )
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'type': self.type.value,
            'strategies': {}
        }
        
        for key, strategy in self.strategies.items():
            if isinstance(strategy, StrategyWINWS):
                result['strategies'][key] = {
                    'instructions': strategy.instructions
                }
            elif isinstance(strategy, StrategyNFQWS):
                result['strategies'][key] = {
                    'nft_tables': strategy.nft_tables,
                    'instructions': strategy.instructions
                }
        
        return result

class StrategyProvider(ABC):
    def __init__(self,dir:str):
        self.dir = dir
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        self.strategies_path = os.path.join(self.dir,"strategies.json")
        self.bundle: StrategiesBundle = StrategiesBundle(StrategyType.NONE,{})

    @abstractmethod
    def update(self):
        ...

    def save(self):
        with open(self.strategies_path,"w") as f:
            json.dump(self.bundle.to_dict(),f,indent=4)

    def load(self):
        with open(self.strategies_path,"r") as f:
            self.bundle = StrategiesBundle.from_dict(json.load(f))

    @property
    def available(self) -> bool:
        return os.path.exists(self.strategies_path)
    
    @property
    def names(self) -> list[str]:
        return list(self.bundle.strategies.keys())
    
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    def metadata(self) -> str:
        return "NO INFO"