from core.strategy import StrategyProvider
from core.zapret_provider import ZapretBinsProvider
import os
import json


class LocalStrategyProvider(StrategyProvider):
    def __init__(self,dir:str):
        super().__init__(dir)
        self.update()

    def update(self):
        self.load()

    @property
    def name(self):
        return os.path.basename(self.dir)
    
class LocalBinsProvider(ZapretBinsProvider):
    def __init__(self,dir:str):
        super().__init__(dir)
        
        with open(os.path.join(self.dir,"index.json"),"r") as f:
            index = json.load(f)

        self.executable = index["executable"]

    @property
    def name(self):
        return os.path.basename(self.dir)
    
    def update(self):
        ...