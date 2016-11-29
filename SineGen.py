import sys
import math
import wave

class WaveFile:
    def __init__(self, filename, nchannels, bitDepth, framerate):
        self.filename = filename
        self.nchannels = nchannels
        self.sampwidth = bitDepth
        self.framerate = framerate
        self.nframes = 0
        self.comptype = 'NONE'
        self.compname = 'not compressed'
        self.audio_bytes = bytes(0)

    def addAudio(self, audio_bytes):
        self.nframes = len(audio_bytes)
        self.audio_bytes = bytes(audio_bytes)

    def saveAudio(self, directory):
        filepath = directory + self.filename
        w = wave.open(filepath,'wb')
        w.setparams((self.nchannels,self.sampwidth,self.framerate,self.nframes,
                     self.comptype,self.compname))
        w.setnframes(self.nframes)
        w.writeframes(self.audio_bytes)
        w.close()

class SineWave:
    def __init__(self, freq=500, samples=44100, 
            bitDepth=24, volume=1.0, length=1):
        self.freq = freq
        self.samples = samples
        self.bitDepth = int(bitDepth/8)
        self.volume = volume
        self.length = length
        self.waveArr = []
        self.buildWave()

    def buildWave(self):
        x = self.samples/self.freq
        y = x / 2
        ampl = pow(2,8*self.bitDepth) - 1
        ampl = (ampl / 2) * self.volume

        for i in range(int(self.length * self.samples)):
            z = i / y
            a = math.sin(z*math.pi)
            b = a * ampl
            self.waveArr.append(int(b))
            
        # print(self.waveArr)
        # input("wait")

    def getBytes(self):
        result = []

        for i in self.waveArr:
            a = self.numToBytes(i,self.bitDepth)
            for j in a:
                result.append(j)

        return result

    #bitdepth of 16 or 24
    def numToBytes(self, num, bitdepth):
        result = []

        if num < 0:
            flipmask = (pow(2,24)-1)
            num = num*-1
            num = num^flipmask

        for i in range(bitdepth):
            bitplace = 8*i
            bitmask = 255 << bitplace
            x = (num & bitmask) >> bitplace
            result.append(x)

        return result

def printArray(arr):
    for i in arr:
        print(i)

def getArgs():
    args = sys.argv

    if len(args) == 1:
        return 0

    freq = 500
    samples = 44100
    bitdepth = 24
    volume = 1
    length = 1
    channels = 1
    filename = "DefaultSineWave.wav"

    for i in range(len(args)):
        a = args[i]
        if a == "-f":
            freq = float(args[i+1])
        elif a == "-s":
            samples = float(args[i+1])
        elif a == "-b":
            bitdepth = float(args[i+1])
        elif a == "-v":
            volume = float(args[i+1])
        elif a == "-l":
            length = float(args[i+1])
        elif a == "-c":
            channels = int(args[i+1])
        elif a == "-n":
            filename = str(args[i+1])
        elif a == "-h" or a == "--help":
            print(""" 
Arg           Description                Default Value
-----------------------------------------------------------
-f          : frequency                 : 500
-s          : samples per second        : 44100
-b          : bit depth                 : 24
-v          : volume from 0.0 to 1.0    : 1.0
-l          : length in seconds 0.0     : 1.0
-c          : channels                  : 1  (2 not supported)
-n          : filename                  : DefaultSineWave.wav
-h, --help  : help

Example:
-f 500 -s 44100 -b 24 -v 0.5 -l 1 -c 1
-----------------------------------------------------------
            """)
            return 0
        
    return (freq,samples,bitdepth,volume,length,channels,filename)

def main():
    vals = getArgs()

    if vals != 0:
        wav = SineWave(vals[0],vals[1],vals[2],vals[3],vals[4])
        # wav = SineWave(100,44100,24,1,2)
        f = WaveFile(vals[6],vals[5],wav.bitDepth,wav.samples)
        f.addAudio(wav.getBytes())
        f.saveAudio("")



if __name__ == "__main__":
    main()