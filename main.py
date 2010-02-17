#!/usr/bin/env python

import struct
import math
import sys

sys.path.append("lib")
import pwave

sample_rate = 48000
n_channels = 1
n_bits = 16
n_samples = sample_rate     # 1 second
base_freq = float(sys.argv[1])

wave_data = ''
wave_header = pwave.make_header(sample_rate, n_samples, n_bits, n_channels)

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
