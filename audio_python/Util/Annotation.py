from Server import RPCServer


def rpcApi(func):
    RPCServer.register(func)
    return func
