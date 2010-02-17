#!/usr/bin/env python

import struct
import math
import sys

sample_rate = 48000
n_channels = 1
n_bits = 16
n_samples = sample_rate     # 1 second
base_freq = float(sys.argv[1])

# Yes, I know about the wave module, but that bastard commits suicide if the
# output is not seekable.  This instead, does no I/O at all.
def get_wave_header(rate, len, width, channels):
    RIFFParse_Format = "4sI4s"
    RIFF_ChunkID = "RIFF"
    RIFF_ChunkSize = 0
    RIFF_Format = "WAVE"

    WAV1Parse_Format = "4sIhhIIhh"
    WAV_Subchunk1ID = "fmt "
    WAV_Subchunk1Size = struct.calcsize(WAV1Parse_Format) - struct.calcsize("4sI")
    WAV_AudioFormat = 1
    WAV_NumChannels = channels
    WAV_SampleRate = rate
    WAV_BitsPerSample = width
    WAV_BlockAlign = 4
    WAV_ByteRate = WAV_SampleRate * WAV_NumChannels + WAV_BitsPerSample/8

    WAV2Parse_Format = "4sI"
    WAV_Subchunk2ID = "data"
    WAV_Subchunk2Size = len * channels * WAV_BitsPerSample/8

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

    return B_RIFF_Header + B_WAV1_Chunk + B_WAV2_Header


wave_data = ''
wave_header = get_wave_header(sample_rate, n_samples, n_bits, n_channels)

base_period = sample_rate/base_freq
fifth_period = (2 * base_period) / 3

for i in range(n_samples):
    base_wave = math.cos(i % base_period * (2 * math.pi/base_period))
    base_amp = (2**14 - 1) * base_wave

    fifth_wave = math.cos(i % fifth_period * (2 * math.pi/fifth_period))
    fifth_amp = (2**14 - 1) * fifth_wave

    wave_data += struct.pack('h', base_amp + fifth_amp)

sys.stdout.write(wave_header)
sys.stdout.write(wave_data)
