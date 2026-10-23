#!/usr/bin/env python3
"""
Kids-Friendly Sound Effects Synthesizer
Generates organic, joyful cartoon sound effects:
- Bubbly Pop (soap bubble burst)
- Splish Splash (gentle water ripple)
- Sparkle Chime (magical glockenspiel glissando)
- Cheerful Giggle / High-Five Ding
"""

import math
import random
import struct
import wave
from pathlib import Path

def write_wav_file(path, samples, sample_rate=44100):
    pcm = bytearray()
    for s in samples:
        val = int(max(-32767, min(32767, s * 32767)))
        pcm.extend(struct.pack('<h', val))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm)

def create_bubble_pop(duration=0.12, sample_rate=44100):
    """Deep bubbly soap pop."""
    n = int(duration * sample_rate)
    samples = []
    for i in range(n):
        t = i / sample_rate
        freq = 300 + 850 * math.sin(math.pi * 0.5 * (t / duration))
        env = math.exp(-t * 38.0)
        # Resonant bubble body
        s = math.sin(2 * math.pi * freq * t) * env * 0.95
        samples.append(s)
    return samples

def create_splish_splash(duration=0.35, sample_rate=44100):
    """Playful water splish-splash sound."""
    n = int(duration * sample_rate)
    samples = []
    # Mix of filtered water droplets + bubbly noise
    droplets = [(800, 0.02), (1200, 0.05), (950, 0.09), (1400, 0.14)]
    for i in range(n):
        t = i / sample_rate
        val = 0.0
        # Droplet chirps
        for f, offset in droplets:
            if t >= offset:
                dt = t - offset
                d_env = math.exp(-dt * 65.0)
                val += math.sin(2 * math.pi * (f + 400 * dt) * dt) * d_env * 0.4
        # Gentle splash noise
        noise_env = math.exp(-t * 14.0) * math.sin(math.pi * (t / duration))
        noise = random.uniform(-1.0, 1.0) * noise_env * 0.25
        samples.append(val + noise)
    return samples

def create_sparkle_chime(duration=0.55, sample_rate=44100):
    """Ascending magic wand bell sparkle."""
    n = int(duration * sample_rate)
    samples = [0.0] * n
    pitches = [1046.50, 1318.51, 1567.98, 2093.00, 2637.02] # C6, E6, G6, C7, E7
    for step_i, freq in enumerate(pitches):
        offset = step_i * 0.08
        start_idx = int(offset * sample_rate)
        for i in range(int(0.3 * sample_rate)):
            idx = start_idx + i
            if idx < n:
                t = i / sample_rate
                env = math.exp(-t * 12.0)
                v = (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * freq * 2.0 * t)) * env * 0.25
                samples[idx] += v
    return samples

def create_high_five_cheer(duration=0.45, sample_rate=44100):
    """Crisp high five clap with sunny bell resonance."""
    n = int(duration * sample_rate)
    samples = []
    for i in range(n):
        t = i / sample_rate
        # Slap impact
        slap_env = math.exp(-t * 40.0)
        slap = random.uniform(-1.0, 1.0) * slap_env * 0.65
        # Sunny bell ring (C6)
        ring_env = math.exp(-t * 9.0)
        ring = math.sin(2 * math.pi * 1046.50 * t) * ring_env * 0.45
        samples.append(slap + ring)
    return samples

def generate_all_kids_sfx(work_dir):
    work_dir = Path(work_dir)
    pop_path = work_dir / "sfx_pop.wav"
    splash_path = work_dir / "sfx_splash.wav"
    chime_path = work_dir / "sfx_chime.wav"
    cheer_path = work_dir / "sfx_cheer.wav"

    write_wav_file(pop_path, create_bubble_pop())
    write_wav_file(splash_path, create_splish_splash())
    write_wav_file(chime_path, create_sparkle_chime())
    write_wav_file(cheer_path, create_high_five_cheer())

    print(f"🫧 Generated kids-friendly sound effects in {work_dir.name}: pop, splash, chime, cheer")
    return {
        "pop": pop_path,
        "splash": splash_path,
        "chime": chime_path,
        "cheer": cheer_path
    }

if __name__ == "__main__":
    generate_all_kids_sfx(".")
