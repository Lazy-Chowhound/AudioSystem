from Server import RPCServer

if __name__ == '__main__':
    from Audio.AudioSetProperty import *
    from Audio.AudioProperty import *
    from Perturbation.AudioProcess import *
    from Perturbation.NoisePattern import *
    from Perturbation.NoisePatternSummary import *

    print("-------rpc sever start-------")
    RPCServer.start()
