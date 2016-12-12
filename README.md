# SineGen
Generate a Sine Wave and save it to a `.wav` file given the following
parameters:
 * Frequency
 * Samples per Second (44.1, 48, 96)
 * Bit-Depth (8, 16, 24)
 * Volume (0.0 - 1.0)
 * Length in Seconds as Decmial
 * Channels (Mono=1, Stereo=2) *`Only 1 channel is currently supported`
 * Filename

## How To Use

The __SineGen__ is simple to use.  If you wish to keep any default values, 
simply do not add a flag for those values.  For a list of possible flags and
default values:

```
$ python3 SineGen.py --help
```

To create a Sine Wave with 1000hzs, 24-bit, 48k, at max volume:

```
$ python3 SineGen.py -f 1000 -b 24 -s 48000 -v 1.0 -n MySineWave.wav 
```

## Dependencies
 * Python 3.x
 * GetArgs (github.com/vindennl48/getargs)

 
