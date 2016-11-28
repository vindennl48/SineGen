import math
import binascii

def sine(sineLength,timePos,amplitude):
    """sineLength: length in time for one complete sine cycle,
       timePos: current position to calculate sine"""
    
    timePos = timePos * 2
    return amplitude*math.sin(timePos*math.pi/sineLength)

def Round(inp, digits):
    formatter = "{0:." + str(digits) + "f}"
    result = formatter.format(inp)
    return int(result)


class SineWave:
    def __init__(self, freq=500, samples=44100, 
            bitDepth=24, volume=1, length=1):
        self.freq = freq
        self.samples = samples
        self.bitDepth = bitDepth
        self.volume = volume
        self.length = length
        self.waveArr = []

    def buildWave(self):
        x = self.samples/self.freq
        y = x / 2
        ampl = pow(2,self.bitDepth) - 1

        for i in range(self.length * self.samples):
            z = i / y
            a = math.sin(z*math.pi)
            b = a * (ampl/2)
            b = b + ampl
            self.waveArr.append(int(b))

    def getBytes(self):
        result = []

        for i in self.waveArr:
            result.append((i).to_bytes(4,byteorder='big'))

        b = bytes(result)

        return b

def printArray(arr):
    for i in arr:
        print(i)

def main():
    wav = SineWave(5000,44100,24,1,1)
    wav.buildWave()

    b = wav.getBytes()


    # for i in wav.getBytes():
    #     print(binascii.hexlify(i))




if __name__ == "__main__":
    main()