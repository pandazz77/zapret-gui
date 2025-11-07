
from providers.flowseal import FlowsealStrategyProvider, FlowsealBinsProvider
from providers.pandazz import PandazzStrategyProvider
from providers.local import LocalStrategyProvider
from core.strategy import StrategyProvider
from core.zapret_provider import ZapretBinsProvider
from core.globals import APPDIR
import os

_BINS_PROVIDERS_DIR = os.path.join(APPDIR,"providers","bins")
_STRATS_PROVIDERS_DIR = os.path.join(APPDIR,"providers","strategy")

_bins_providers: dict[str,ZapretBinsProvider] = {}
_strategy_providers: dict[str,StrategyProvider] = {}

def _SetupBinsProviders():
    # DEFAULT =========
    def setupStandard(cls,name):
        path = os.path.join(_BINS_PROVIDERS_DIR,name)
        _bins_providers[name] = cls(path)

    setupStandard(FlowsealBinsProvider,FlowsealBinsProvider.NAME)
    # =================

def _SetupStrategiesProviders():
    # DEFAULT =========
    def setupStandard(cls,name):
        path = os.path.join(_STRATS_PROVIDERS_DIR,name)
        _strategy_providers[name] = cls(path)

    setupStandard(FlowsealStrategyProvider,FlowsealStrategyProvider.NAME)
    setupStandard(PandazzStrategyProvider,PandazzStrategyProvider.NAME)
    # =================

    # LOCALS ==========
    os.listdir(_STRATS_PROVIDERS_DIR)
    for dir in os.listdir(_STRATS_PROVIDERS_DIR):
        if dir not in _strategy_providers:
            fullpath = os.path.join(_STRATS_PROVIDERS_DIR,dir)
            provider = LocalStrategyProvider(fullpath)
            _strategy_providers[provider.name] = provider
    # =================

def SetupProviders(): # MUST BE INITIALISED
    _SetupBinsProviders()
    _SetupStrategiesProviders()

def GetBinsProvider(name:str) -> ZapretBinsProvider:
    return _bins_providers[name]

def GetStrategyProvider(name:str) -> StrategyProvider:
    return _strategy_providers[name]

def AvailableBinsProviders() -> list[str]:
    return list(_bins_providers.keys())

def AvailableStrategyProviders() -> list[str]:
    return list(_strategy_providers.keys())



SetupProviders()