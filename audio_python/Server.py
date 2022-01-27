from xmlrpc.server import SimpleXMLRPCServer


class RPCServer:
    rpcServer = SimpleXMLRPCServer(("localhost", 8081), allow_none=True)

    @staticmethod
    def register(func):
        RPCServer.rpcServer.register_function(func)

    @staticmethod
    def start():
        RPCServer.rpcServer.serve_forever()
