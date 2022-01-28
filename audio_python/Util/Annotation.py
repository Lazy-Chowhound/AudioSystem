from Server import RPCServer


def rpcApi(func):
    RPCServer.register(func)
    print("%s has registered" % func.__name__)
    return func
