#!/usr/bin/env python

import struct
import math
import sys
import time
import random

sys.path.append("lib")
import pwave

sample_rate = 48000
n_channels = 1
n_bits = 16
n_samples = sample_rate     # 1 second
base_freq = float(sys.argv[1])

def rand_wave(n):
    wav = struct.pack('h', 0)
    cur = 0
    random.seed(time.time())
    amplitude = 0

    for i in xrange(n):
        low = cur - 300
        hig = cur + 300
        if cur > 2**15 - 2:     hig = cur
        elif cur > 2**14 - 2:   hig = cur + 100
        elif cur > 2**13 - 2:   hig = cur + 200
        elif cur < 2 - 2**15:   low = cur
        elif cur < 2 - 2**14:   low = cur + 100
        elif cur < 2 - 2**13:   low = cur + 200

        cur = random.randrange(low, hig + 1)
        wav += struct.pack('h', cur)
        amplitude = max(amplitude, cur)

    print >> sys.stderr, amplitude
    return wav


wave_data = ''
wave_header = pwave.make_header(sample_rate, n_samples*100, n_bits, n_channels)

base_period = sample_rate/base_freq
fifth_period = (2 * base_period) / 3

for i in range(n_samples):
    base_wave = math.cos(i % base_period * (2 * math.pi/base_period))
    base_amp = (2**14 - 1) * base_wave

    fifth_wave = math.cos(i % fifth_period * (2 * math.pi/fifth_period))
    fifth_amp = (2**14 - 1) * fifth_wave

    wave_data += struct.pack('h', base_amp + fifth_amp)

sys.stdout.write(wave_header)
#sys.stdout.write(wav)
sys.stdout.write(rand_wave(n_samples*100))
