from core.strategy import StrategyProvider, StrategiesBundle, StrategyType
import core.github_utils as github
import os
import json


USERNAME = "pandazz77"
REPONAME = "zapret-pndz-assets"

def download_folder(gh_folder,output_folder):
    paths = github.get_files_list(USERNAME,REPONAME,gh_folder,branch="master")
    for path in paths:
        filename = path.split("/")[-1]
        github.download_file(USERNAME,REPONAME, path,os.path.join(output_folder,filename),branch="master")


class PandazzStrategyProvider(StrategyProvider):
    NAME = "PANDAZZ"

    def __init__(self,dir:str):
        super().__init__(dir)
        self.bundle.type = StrategyType.WINWS
        self.lists_path = os.path.join(self.dir,"lists")
        self.bins_path = os.path.join(self.dir,"bins")

        os.makedirs(self.lists_path,exist_ok=True)
        os.makedirs(self.bins_path,exist_ok=True)

    
    def update(self):
        download_folder("strategies/lists",self.lists_path)
        download_folder("strategies/bins",self.bins_path)

        strategies_raw = github.get_file_content_raw(USERNAME,REPONAME,"strategies/strategies.json",branch="master").decode('utf-8')
        path = os.path.abspath(self.dir).replace("\\","/")
        strategies_raw = strategies_raw.replace("@PATH@",path)
        self.bundle.strategies = StrategiesBundle.from_dict(json.loads(strategies_raw))
        self.save()

    @property
    def name(self) -> str:
        return self.NAME
