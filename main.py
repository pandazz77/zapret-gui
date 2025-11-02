import os
from flowseal_parser import download_bins, download_lists, parse_strategy, FlowsealBinsProvider, FlowsealStrategyProvider
import time


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)

    def test0():
        path = os.path.normpath("./.untracked")
        os.makedirs(path,exist_ok=True)
        download_lists(path)
        download_bins(path)

    def test1():
        import json
        path = os.path.normpath("./.untracked/general (ALT).bat")
        with open(path,"r") as f:
            strategy = parse_strategy(f.read(),current_dir,current_dir)
            print(json.dumps(strategy,indent=4))

    def test2():
        fsp = FlowsealStrategyProvider(".untracked\\flowseal")
        fsp.update()

    def test3():
        fsp = FlowsealStrategyProvider(".untracked\\flowseal")
        fsp.load()
        print(fsp.strategies)

    def test4():
        fbp = FlowsealBinsProvider(".untracked\\flowseal_bins")
        print("available:",fbp.available)
        fbp.update()
        print("available:",fbp.available)

    def test5():
        from zapret_handler import ZapretHandler
        fsp = FlowsealStrategyProvider(".untracked\\flowseal")
        fbp = FlowsealBinsProvider(".untracked\\flowseal_bins")
        fsp.load()
        zapret = ZapretHandler(fbp,fsp)
        
        result = zapret.autosearch()
        if result:
            time.sleep(0.5)
            print(result)
            input("blockcheck successed, press enter to exit:")

    # test0()
    # test1()
    # test2()
    # test3()
    # test4()
    test5()