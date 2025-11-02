
from providers.flowseal_parser import FlowsealStrategyProvider, FlowsealBinsProvider
from core.strategy import StrategyProvider
from core.zapret_provider import ZapretBinsProvider
import os

FLOWSEAL = "FLOWSEAL"

_bins_providers = {
    FLOWSEAL: FlowsealBinsProvider
}

_strategy_providers = {
    FLOWSEAL: FlowsealStrategyProvider
}

APPDIR = os.path.join(os.environ['APPDATA'],"zapret_gui")
os.makedirs(APPDIR,exist_ok=True)

def GetBinsProvider(name:str) -> ZapretBinsProvider:
    path = os.path.join(APPDIR,"providers","bins",name)
    os.makedirs(path,exist_ok=True)
    return _bins_providers[name](path)

def GetStrategyProvider(name:str) -> StrategyProvider:
    path = os.path.join(APPDIR,"providers","strategy",name)
    os.makedirs(path,exist_ok=True)
    return _strategy_providers[name](path)

def AvailableBinsProviders() -> list[str]:
    return list(_bins_providers.keys())

def AvailableStrategyProviders() -> list[str]:
    return list(_strategy_providers.keys())