import os
from abc import abstractmethod, ABC
import shutil


class ZapretBinsProvider(ABC):
    def __init__(self,dir:str):
        self.dir:str = dir
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        self.executable: str = None # NEED TO BE SETTED in inherrited __init__

    @abstractmethod
    def update(self):
        ...

    def clear(self):
        shutil.rmtree(self.dir)
        os.mkdir(self.dir)

    def full_update(self):
        self.clear()
        self.update()

    @property
    def available(self) -> bool:
        if not self.executable: return False
        return os.path.exists(self.executable)