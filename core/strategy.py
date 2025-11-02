import json
import os
from abc import abstractmethod, ABC
from typing import TypedDict


class Strategy(TypedDict):
    instructions: list[str]

class StrategyProvider(ABC):
    def __init__(self,dir:str):
        self.dir = dir
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        self.strategies_path = os.path.join(self.dir,"strategies.json")
        self.strategies:dict[str,Strategy] = {}

    @abstractmethod
    def update(self):
        ...

    def save(self):
        with open(self.strategies_path,"w") as f:
            json.dump(self.strategies,f,indent=4)

    def load(self):
        with open(self.strategies_path,"r") as f:
            self.strategies = json.load(f)

    @property
    def available(self) -> bool:
        return os.path.exists(self.strategies_path)
    
    @property
    def names(self) -> list[str]:
        return list(self.strategies.keys())