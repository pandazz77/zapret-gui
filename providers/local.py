from core.strategy import StrategyProvider
from core.zapret_provider import ZapretBinsProvider
import os


class LocalStrategyProvider(StrategyProvider):
    def __init__(self,dir:str):
        super().__init__(dir)
        self.update()

    def update(self):
        self.load()

    @property
    def name(self):
        return os.path.basename(self.dir)
    