import logging
import os


APPDIR = os.path.join(os.environ['APPDATA'],"zapret_gui")
os.makedirs(APPDIR,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s]  %(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(APPDIR,'zapret_gui.log'))
    ]
)