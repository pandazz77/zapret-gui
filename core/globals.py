import logging
import os
import atexit
from core.settings import Settings

VERSION = "0.1"
APPDIR = os.path.join(os.environ['APPDATA'],"zapret_gui")
settings: Settings = None

os.makedirs(APPDIR,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s]  %(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(APPDIR,'zapret_gui.log'))
    ]
)

Settings.setup(APPDIR)
settings = Settings(
    preffered_bins_provider="FLOWSEAL",
    preffered_strategy_provider="FLOWSEAL",
    preffered_strategy=None
)
settings.load()
atexit.register(settings.save)