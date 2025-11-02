from zapret_provider import ZapretBinsProvider
from strategy import StrategyProvider, Strategy
import subprocess
import os
import atexit
import requests


class ZapretHandler:
    def __init__(self,bin:ZapretBinsProvider,strategy:StrategyProvider):
        self.bin = bin
        self.strategy = strategy
        self.process = subprocess.Popen
        atexit.register(self.stop)

    def start(self,strategy):
        strategy: Strategy = self.strategy.strategies[strategy]
        instructions = strategy["instructions"]
        print(instructions)
        self.process = subprocess.Popen(
            [self.bin.executable,*instructions],
            cwd=os.path.dirname(self.bin.executable)
        )

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def blockcheck(self,retries=5) -> bool:
        print("blockchecking...")
        for _ in range(retries):
            try:
                resp = requests.get("https://discord.com",timeout=3)
            except Exception:
                continue
            print(resp.status_code)
            if resp.status_code == 200: return True

        return False
    
    def autosearch(self) -> str:
        for name in self.strategy.strategies.keys():
            self.start(name)
            if self.blockcheck():
                return name
            else:
                self.stop()