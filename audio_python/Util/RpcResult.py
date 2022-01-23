class RpcResult:
    def __init__(self, code, data):
        self.code = code
        self.data = data

    @staticmethod
    def ok(data):
        return RpcResult(200, data)
