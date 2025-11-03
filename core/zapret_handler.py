from core.zapret_provider import ZapretBinsProvider
from core.strategy import StrategyProvider, Strategy
import subprocess
import threading
import os
import atexit
import requests
import logging
from enum import Enum

class ZapretStatus(Enum):
    STOPPED = 0,
    STARTING = 1,
    STARTED = 2

def _default_status_hook(status:ZapretStatus):
    print("New Zapret status:",status.name)

class ZapretHandler:
    def __init__(self,bin:ZapretBinsProvider,strategy:StrategyProvider):
        self.bin = bin
        self.strategy = strategy
        self.process: subprocess.Popen = None
        self.status_hook: callable = _default_status_hook
        self.status: ZapretStatus = ZapretStatus.STOPPED
        self.logger = logging.getLogger("ZapretHandler")
        atexit.register(self.stop)

    def start(self,strategy):
        self._status_hook_router(ZapretStatus.STARTING)
        strategy: Strategy = self.strategy.strategies[strategy]
        instructions = strategy["instructions"]
        self.process = subprocess.Popen(
            [self.bin.executable,*instructions],
            cwd=os.path.dirname(self.bin.executable),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        self._stdout_hook = threading.Thread(target=self._process_stdout_hook,daemon=True)
        self._stdout_hook.start()

    def _process_stdout_hook(self):
        for line in self.process.stdout:
            line:str = line.rstrip('\n\r')
            self.logger.debug(line)
            if "capture is started" in line:
                self.logger.info("started")
                self._status_hook_router(ZapretStatus.STARTED)
        self.logger.info("stopped")

    def _status_hook_router(self,status:ZapretStatus):
        self.status = status
        self.status_hook(status)

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self._status_hook_router(ZapretStatus.STOPPED)

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