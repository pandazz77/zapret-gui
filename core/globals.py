import logging
import os
import atexit
from core.settings import Settings
import platform
from providers.flowseal_parser import FlowsealStrategyProvider, FlowsealBinsProvider

VERSION = "0.3"

if platform.system() == "Windows": 
    APPDIR = os.path.join(os.environ['APPDATA'],"zapret_gui")
elif platform.system() == "Linux":
    APPDIR = os.path.join(os.environ['HOME'],".config","zapret_gui")

settings: Settings = None

os.makedirs(APPDIR,exist_ok=True)

def setup_logging(level:str):
    logging.basicConfig(
        level=level,
        format='[%(name)s]  %(asctime)s - %(levelname)s %(filename)s:%(lineno)d - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(APPDIR,'zapret_gui.log'))
        ]
    )

Settings.setup(APPDIR)
settings = Settings(
    preffered_bins_provider=FlowsealBinsProvider.NAME,
    preffered_strategy_provider=FlowsealStrategyProvider.NAME,
    preffered_strategy=None
)
settings.load()
atexit.register(settings.save)