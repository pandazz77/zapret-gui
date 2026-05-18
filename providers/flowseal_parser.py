import core.github_utils as github
import time
import logging
import os
from pathlib import Path
from core.strategy import Strategy, Dict, StrategyProvider, Version
from core.zapret_provider import ZapretBinsProvider
from enum import Enum

class GameFilter(Enum):
    NONE = 0
    ALL = 1
    TCP = 2
    UDP = 3
    

USERNAME = "Flowseal"
REPONAME = "zapret-discord-youtube"
GAMEFILTER_ENABLED = "1024-65535"
GAMEFILTER_DISABLED = "12"

def get_strategies_paths():
    """ 
        get .bat strategies floseals's github paths
    """
    files = github.get_files_list(USERNAME,REPONAME,path="")
    
    return list(filter(lambda path: path.endswith(".bat") and "general" in path,files))

def get_raw_strategies_contents(paths:list[str]):
    result = {}

    for path in paths:
        strategy_name = path.split("/")[-1].removesuffix(".bat")
        content = github.get_file_content_raw(USERNAME,REPONAME,file_path=path).decode("utf-8")
        result[strategy_name] = content
        time.sleep(0.5)
    return result

def create_user_lists(output_folder:str):
    filenames = (
        "ipset-exclude-user.txt",
        "list-general-user.txt",
        "list-exclude-user.txt"
    )
    for name in filenames:
        path = os.path.join(output_folder,name)
        if not os.path.exists(path):
            with open(path,"w") as f:
                f.write("domain.example.abc")

def download_lists(output_folder:str):
    paths = filter(lambda path: path.endswith(".txt"),github.get_files_list(USERNAME,REPONAME,"lists"))
    for path in paths:
        filename = path.split("/")[-1]
        github.download_file(USERNAME,REPONAME, path,os.path.join(output_folder,filename))

    create_user_lists(output_folder)

def download_bins(output_folder:str):
    paths = filter(lambda path: path.endswith(".bin"),github.get_files_list(USERNAME,REPONAME,"bin"))
    for path in paths:
        filename = path.split("/")[-1]
        github.download_file(USERNAME,REPONAME, path,os.path.join(output_folder,filename))

def enclose_sep(path:str):
    if not path.endswith(os.path.sep): path += os.path.sep
    return path

def parse_strategy(strategy_raw:str,lists_path:str,bins_paths:str,gamefilter_mode:GameFilter=GameFilter.NONE) -> list[str]:
    match gamefilter_mode:
        case GameFilter.NONE:
            gamefilter = GAMEFILTER_DISABLED
            gamefilter_udp = GAMEFILTER_DISABLED
            gamefilter_tcp = GAMEFILTER_DISABLED
        case GameFilter.ALL:
            gamefilter = GAMEFILTER_ENABLED
            gamefilter_udp = GAMEFILTER_ENABLED
            gamefilter_tcp = GAMEFILTER_ENABLED
        case GameFilter.TCP:
            gamefilter = GAMEFILTER_ENABLED
            gamefilter_udp = GAMEFILTER_DISABLED
            gamefilter_tcp = GAMEFILTER_ENABLED
        case GameFilter.UDP:
            gamefilter = GAMEFILTER_ENABLED
            gamefilter_udp = GAMEFILTER_ENABLED
            gamefilter_tcp = GAMEFILTER_DISABLED


    lists_path = enclose_sep(os.path.abspath(lists_path))
    bins_paths = enclose_sep(os.path.abspath(bins_paths))

    # prepare instructions
    strategy_raw = strategy_raw[strategy_raw.find('--'):]
    strategy_raw = strategy_raw.replace("^","")
    strategy_raw = strategy_raw.replace("\n","")
    strategy_raw = strategy_raw.replace('"',"'")

    # replace vars
    strategy_raw = strategy_raw.replace(r"%GameFilter%",gamefilter)
    strategy_raw = strategy_raw.replace(r"%GameFilterTCP%",gamefilter_tcp)
    strategy_raw = strategy_raw.replace(r"%GameFilterUDP%",gamefilter_udp)
    strategy_raw = strategy_raw.replace(r"%LISTS%",lists_path)
    strategy_raw = strategy_raw.replace(r"%BIN%",bins_paths)

    # checking
    if "%" in strategy_raw:
        ind1 = strategy_raw.find("%")
        ind2 = ind1+strategy_raw[ind1+1:].find("%")+1
        logging.warning(f"UNPARSED BAT VARIABLE FOUND: {strategy_raw[ind1:ind2+1]}")

    return strategy_raw.split(" ")


class FlowsealStrategyProvider(StrategyProvider):
    def __init__(self,dir:str):
        super().__init__(dir)
        self.lists_path = os.path.join(self.dir,"lists")
        self.bins_path = os.path.join(self.dir,"bins")

        os.makedirs(self.lists_path,exist_ok=True)
        os.makedirs(self.bins_path,exist_ok=True)

    
    def update(self):
        download_lists(self.lists_path)
        download_bins(self.bins_path)
        strategies_paths = get_strategies_paths()
        raw_strategies = get_raw_strategies_contents(strategies_paths)
        commit, date = github.get_last_commit(USERNAME,REPONAME)
        version = Version(commit,date)

        strategies: Dict[str,Strategy] = {}

        for name, instructions_raw in raw_strategies.items():
            instructions = parse_strategy(instructions_raw,self.lists_path,self.bins_path)
            strategies[name] = Strategy(instructions)

        self._update(
            strategies,
            version
        )
        self.save()

class FlowsealBinsProvider(ZapretBinsProvider):
    def __init__(self, dir):
        super().__init__(dir)
        self.executable = Path(self.dir,"winws.exe")

    def update(self):
        output_folder = self.dir
        paths = filter(lambda path: path.endswith((".dll",".sys",".exe")),github.get_files_list(USERNAME,REPONAME,"bin"))
        for path in paths:
            filename = path.split("/")[-1]
            github.download_file(USERNAME,REPONAME, path,os.path.join(output_folder,filename))
