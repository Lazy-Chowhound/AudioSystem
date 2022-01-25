from xmlrpc.server import SimpleXMLRPCServer


class RPCServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.rpcServer = SimpleXMLRPCServer((self.ip, self.port), allow_none=True)

    def register(self, func):
        self.rpcServer.register_function(func)

    def start(self):
        self.rpcServer.serve_forever()
