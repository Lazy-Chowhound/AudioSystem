from xmlrpc.server import SimpleXMLRPCServer


class RPCServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.rpcServer = None

    def start(self, function_list):
        self.rpcServer = SimpleXMLRPCServer((self.ip, self.port))
        for func in function_list:
            self.rpcServer.register_function(func)
        self.rpcServer.serve_forever()

