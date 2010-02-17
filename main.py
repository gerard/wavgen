#!/usr/bin/env python

import struct
import math
import sys

sound_len = 2048
sample_rate = 48000
n_channels = 1
n_samples = sample_rate     # 1 second
base_freq = float(sys.argv[1])

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

base_period = sample_rate/base_freq
fifth_period = (2 * base_period) / 3

for i in range(n_samples):
    base_wave = math.cos(i % base_period * (2 * math.pi/base_period))
    base_amp = (2**14 - 1) * base_wave

    fifth_wave = math.cos(i % fifth_period * (2 * math.pi/fifth_period))
    fifth_amp = (2**14 - 1) * fifth_wave

    sys.stdout.write(struct.pack('h', base_amp + fifth_amp))

