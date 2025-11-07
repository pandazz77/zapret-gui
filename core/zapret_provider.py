import os
from abc import abstractmethod, ABC


class ZapretBinsProvider(ABC):
    def __init__(self,dir:str):
        self.dir:str = dir
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        self.executable: str = None # NEED TO BE SETTED in inherrited __init__

    @abstractmethod
    def update(self):
        ...

    @property
    def available(self) -> bool:
        if not self.executable: return False
        return os.path.exists(self.executable)
    
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    def metadata(self) -> str:
        return "NO INFO"