import json
import os
from abc import abstractmethod, ABC
from typing import TypedDict, List, Dict
from .edataclasses import EDataclass
from dataclasses import dataclass
import shutil


@dataclass
class Strategy(EDataclass):
    instructions: List[str]

@dataclass
class StrategiesSet(EDataclass):
    strategies: Dict[str,Strategy]
    version: str|None

class StrategyProvider(ABC):
    def __init__(self,dir:str):
        self.dir = dir
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        self.strategies_path = os.path.join(self.dir,"strategies.json")
        self._strategies_set: StrategiesSet = StrategiesSet({},None)

    @property
    def strategies(self) -> Dict[str,Strategy]:
        return self._strategies_set.strategies
    
    @property
    def version(self) -> str:
        return self._strategies_set.version

    @abstractmethod
    def update(self):
        ...

    def _update(self, strategies: Dict[str,Strategy], version: str):
        self._strategies_set.strategies = strategies
        self._strategies_set.version = version

    def clear(self):
        shutil.rmtree(self.dir)
        os.mkdir(self.dir)

    def full_update(self):
        self.clear()
        self.update()

    def save(self):
        with open(self.strategies_path,"w") as f:
            json.dump(self._strategies_set.to_dict(),f,indent=4)

    def load(self):
        with open(self.strategies_path,"r") as f:
            self._strategies_set = StrategiesSet.from_dict(json.load(f))

    @property
    def available(self) -> bool:
        return os.path.exists(self.strategies_path)
    
    @property
    def names(self) -> list[str]:
        return list(self.strategies.keys())