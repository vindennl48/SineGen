#! python3

import sys
import math
import wave

class WaveFile:
    #Create and save a wav file

    #nchannels: 1 for mono, 2 for stereo
    #bitDepth : 8, 16, 24 bits per sample
    #samples  : sample rate, 44100, 48000, 96000, 128000, etc..
    def __init__(self, filename, nchannels, bitDepth, samples):
        self.filename = filename
        self.nchannels = nchannels
        self.sampwidth = bitDepth
        self.samples = samples
        self.nframes = 0  #this is set in func addAudio()
        self.comptype = 'NONE'  #needed for wav header, ignore
        self.compname = 'not compressed'  #needed for wav header, ignore
        self.audio_bytes = bytes(0)

    #Adds audio bytes to the audio file.
    #audio_bytes : takes a 'bytes()' object
    #automatically sets number of frames for wav header
    def addAudio(self, audio_bytes):
        self.nframes = len(audio_bytes)
        self.audio_bytes = bytes(audio_bytes)

    #directory: location of saved file
    def saveAudio(self, directory):
        filepath = directory + self.filename
        w = wave.open(filepath,'wb')
        w.setparams((self.nchannels,self.sampwidth,self.samples,self.nframes,
                     self.comptype,self.compname))
        w.setnframes(self.nframes)
        w.writeframes(self.audio_bytes)
        w.close()

class SineWave:
    #Generates sine wave object

    #freq : frequency in hz 1 - (samplerate/2)
    #samples : bytes per second, 44100, 48000, 96000, 128000, etc..
    #bitDepth : 8,16,24 bits per sample
    #volume : 0.0 to 1.0 percentage of max bitdepth
    #length : amount of seconds as float
    def __init__(self, freq=500, samples=44100, 
            bitDepth=24, volume=1.0, length=1):
        self.freq = freq
        self.samples = samples
        self.bitDepth = int(bitDepth/8) #num of bytes in sample
        self.volume = volume
        self.length = length
        self.waveArr = []
        self.buildWave()

    #Generate sine wave
    def buildWave(self):
        #calculate distribution of samples per hz
        x = self.samples/self.freq
        y = x / 2

        #calcuulate amplitude of sine wave compared to max
        #  bit depth
        ampl = pow(2,8*self.bitDepth) - 1
        ampl = (ampl / 2) * self.volume

        for i in range(int(self.length * self.samples)):
            #create samples for alloted length
            z = i / y
            a = math.sin(z*math.pi)
            b = a * ampl
            self.waveArr.append(int(b))

    def getBytes(self):
        #returns the samples for the sine wave generated
        #  as a list
        result = []

        for i in self.waveArr:
            a = self.numToBytes(i,self.bitDepth)
            for j in a:
                result.append(j)

        return result

    #bitdepth : number of bytes in sample (1,2,3)
    def numToBytes(self, num, bitdepth):
        #converts num to compatable bytes for 'bytes()' object
        #converts negative num to binary negative
        
        result = []

        if num < 0:
            #if num is negative
            #note: no number can be higher than half the
            #  current bitrate so no safety measures need
            #  to be taken for finding the most significant
            #  bit.

            #create bitmask to flip binary string
            flipmask = (pow(2,24)-1)
            #remove negative sign from python int
            num = num*-1
            #apply bitmask to flip binary string
            num = num^flipmask
            #add one to flipped string to complete negation
            num = num + 1

        for i in range(bitdepth):
            #convert num to 3 separate bytes from -128 to 127

            #calculate bitshift
            bitplace = 8*i

            #create bitmask
            bitmask = 255 << bitplace

            #apply bitmask to get byte
            x = (num & bitmask) >> bitplace
            result.append(x)

        return result

def getArgs():
    #simple retrieval of args in terminal
    
    args = sys.argv

    #if no args then exit program
    if len(args) == 1:
        return 0

    #default values
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
        #if no args are present in 'getArgs()', exit program

        #create 'SineWave()' obj
        wav = SineWave(vals[0],vals[1],vals[2],vals[3],vals[4])
        # wav = SineWave(freq,samples,bitdepth(16-24),volume,seconds)

        #create wave saving file obj
        f = WaveFile(vals[6],vals[5],wav.bitDepth,wav.samples)
        # f = WaveFile(filename,nchannels,bitdepth,samples)

        f.addAudio(wav.getBytes())

        #leave default directory in same file as py program
        f.saveAudio("")



if __name__ == "__main__":
    main()
