import importlib
from Server import RPCServer
from Util.PackageUtil import PackageUtil

if __name__ == '__main__':
    for module in PackageUtil.getPackageModule():
        importlib.import_module(module)
    print("-------rpc sever start-------")
    RPCServer.start()
