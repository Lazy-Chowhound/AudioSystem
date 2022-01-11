from AudioProperty import *
from AudioSetProperty import *
from Server import RPCServer
from NoisePatternSummary import *

if __name__ == '__main__':
    rpcServer = RPCServer("localhost", 8081)
    print("-------rpc sever start-------")
    rpcServer.start([getAudioSet, getAudio, getWaveForm, getMelSpectrum, removeImage,
                     getNoisePatternSummary, getNoisePatternDetail])
