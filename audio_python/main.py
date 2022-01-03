from AudioSetProperty import *
from Server import RPCServer

if __name__ == '__main__':
    rpcServer = RPCServer("localhost", 8081)
    print("-------rpc sever start-------")
    rpcServer.start([getAudioSet])
