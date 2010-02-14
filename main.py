#!/usr/bin/env python

import random
import struct
import math
import sys

sound_len = 2048
sample_rate = 8000
n_channels = 1
n_samples = 10000

RIFFParse_Format = "4sI4s"
RIFF_ChunkID = "RIFF"
RIFF_ChunkSize = 0
RIFF_Format = "WAVE"

WAV1Parse_Format = "4sIhhIIhh"
WAV_Subchunk1ID = "fmt "
WAV_Subchunk1Size = struct.calcsize(WAV1Parse_Format) - struct.calcsize("4sI")
WAV_AudioFormat = 1
WAV_NumChannels = n_channels
WAV_SampleRate = sample_rate
WAV_BitsPerSample = 16
WAV_BlockAlign = 4
WAV_ByteRate = WAV_SampleRate * WAV_NumChannels + WAV_BitsPerSample/8

WAV2Parse_Format = "4sI"
WAV_Subchunk2ID = "data"
WAV_Subchunk2Size = n_samples * n_channels * WAV_BitsPerSample/8

RIFF_ChunkSize = 4 + (8 + WAV_Subchunk1Size) + (8 + WAV_Subchunk2Size)

B_RIFF_Header = struct.pack(RIFFParse_Format,
                            RIFF_ChunkID,
                            RIFF_ChunkSize,
                            RIFF_Format)

B_WAV1_Chunk = struct.pack(WAV1Parse_Format,
                           WAV_Subchunk1ID,
                           WAV_Subchunk1Size,
                           WAV_AudioFormat,
                           WAV_NumChannels,
                           WAV_SampleRate,
                           WAV_ByteRate,
                           WAV_BlockAlign,
                           WAV_BitsPerSample)

B_WAV2_Header = struct.pack(WAV2Parse_Format,
                            WAV_Subchunk2ID,
                            WAV_Subchunk2Size)

sys.stdout.write(B_RIFF_Header)
sys.stdout.write(B_WAV1_Chunk)
sys.stdout.write(B_WAV2_Header)

for i in range(n_samples):
    sample = (2**15) * math.sin((i%40) * (math.pi/40))      # 200 Hz signal
    sys.stdout.write(struct.pack('H', sample))

