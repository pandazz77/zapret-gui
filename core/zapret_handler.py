from core.zapret_provider import ZapretBinsProvider
from core.strategy import StrategyProvider, Strategy
from core.utils import get_pid_by_name
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

_instance:"ZapretHandler" = None

class ZapretHandler:
    def __init__(self,bin:ZapretBinsProvider,strategy:StrategyProvider):
        global _instance
        if _instance:
            raise Exception("ZapretHandler already initialized")
        _instance = self

        self.bin = bin
        self.strategy = strategy
        self.process: subprocess.Popen = None
        self.status_hook: callable = _default_status_hook
        self.status: ZapretStatus = ZapretStatus.STOPPED
        self.logger = logging.getLogger("ZapretHandler")
        atexit.register(self.stop) 

    @staticmethod
    def get_instance() -> "ZapretHandler":
        return _instance

    def start(self,strategy):
        if existing_pid:= get_pid_by_name(os.path.basename(self.bin.executable)):
            self.logger.warn(f"{os.path.basename(self.bin.executable)} already exists with pid {existing_pid}. Killing...")
            os.kill(existing_pid,-1)

        self._status_hook_router(ZapretStatus.STARTING)
        strategy: Strategy = self.strategy.strategies[strategy]
        instructions = strategy["instructions"]
        self.process = subprocess.Popen(
            [self.bin.executable,*instructions],
            cwd=os.path.dirname(self.bin.executable),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW
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
        self.logger.debug("blockchecking...")
        for _ in range(retries):
            try:
                resp = requests.get("https://discord.com",timeout=3)
            except Exception as e:
                self.logger.info(f"blockchecking exception: {e}")
                continue
            self.logger.info(f"blockchecking status: {resp.status_code}")
            if resp.status_code == 200: return True

        return False
    
    def autosearch(self) -> str:
        for name in self.strategy.strategies.keys():
            self.start(name)
            if self.blockcheck():
                return name
            else:
                self.stop()