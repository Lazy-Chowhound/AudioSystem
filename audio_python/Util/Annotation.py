# 函数列表
from Server import RPCServer

rpcServer = RPCServer("localhost", 8081)


# 自定义注解
def rpcApi():
    def decorate(fn):
        rpcServer.register(fn)
        return fn

    return decorate
