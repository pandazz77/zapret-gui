
from providers.flowseal import FlowsealStrategyProvider, FlowsealBinsProvider
from providers.pandazz import PandazzStrategyProvider
from core.strategy import StrategyProvider
from core.zapret_provider import ZapretBinsProvider
from core.globals import APPDIR
import os

_bins_providers = {
    FlowsealBinsProvider.NAME: FlowsealBinsProvider
}

_strategy_providers = {
    PandazzStrategyProvider.NAME: PandazzStrategyProvider,
    FlowsealStrategyProvider.NAME: FlowsealStrategyProvider,
}

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