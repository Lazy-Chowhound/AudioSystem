from Audio.AudioProperty import *
from Audio.AudioSetProperty import *
from Perturbation.NoisePatternSummary import *
from Server import RPCServer

if __name__ == '__main__':
    rpcServer = RPCServer("localhost", 8081)
    print("-------rpc sever start-------")
    rpcServer.start([getAudioSet, getAudioSetList, getAudio, getWaveForm, getMelSpectrum, removeImage,
                     getNoisePatternSummary, getNoisePatternDetail])
