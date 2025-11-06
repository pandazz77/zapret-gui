from functools import wraps
import subprocess
import platform
import queue
import threading
from typing import Callable


def get_pid_by_name_windows(process_name: str) -> int | None:
    result = subprocess.run(
        ['tasklist', '/FI', f'IMAGENAME eq {process_name}', '/FO', 'CSV'],
        capture_output=True,
        text=True,
        check=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    if result.stdout.count("\n") == 1:
        return None
    header, content = result.stdout.strip().split('\n')
    content = map(lambda s: s.replace("\"",""),content.split(","))
    image_name, pid, session_name, session, mem_usage = content
    return int(pid)

def get_pid_by_name(process_name: str) -> int | None:
    if platform.system() == "Windows":
        return get_pid_by_name_windows(process_name)
    

class TaskQueue:
    def __init__(self):
        self._tasks = queue.Queue()
        self._thread:threading.Thread = None

    def add(self,target:Callable,*args,**kwargs):
        self._tasks.put((target,args,kwargs))
        if self._thread is None:
            self._thread = threading.Thread(target=self._task_loop,daemon=True) 
            self._thread.start()

    def _task_loop(self):
        while not self._tasks.empty():
            target,args,kwargs = self._tasks.get()
            target(*args,**kwargs)
        else:
            self._thread = None

def threaded(func: Callable) -> Callable:
    """
    Run function/method in thread

    Returns: Thread
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper