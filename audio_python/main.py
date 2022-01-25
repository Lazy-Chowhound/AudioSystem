from Audio.AudioProperty import *
from Audio.AudioSetProperty import *
from Perturbation.NoisePatternSummary import *
from Perturbation.NoisePattern import *
from Server import RPCServer

if __name__ == '__main__':
    rpcServer = RPCServer("localhost", 8081)
    print("-------rpc sever start-------")
    rpcServer.start([getAudioSet, getAudioSetList, getAudio, getWaveForm, getMelSpectrum, removeImage,
                     getNoisePatternSummary, getNoisePatternDetail, getAudioSetPattern,
                     add_gaussian_noise, add_sound_level, add_natural_sounds, add_animal, add_sound_of_things,
                     removeFormerAudio])
