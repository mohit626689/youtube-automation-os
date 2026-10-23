#!/usr/bin/env python3
"""
Preschool Acoustic Nursery Rhyme Composer
Uses physical acoustic modeling:
- Karplus-Strong string synthesis (Ukulele & Upright Bass)
- Modal metallic resonance (Glockenspiel & Xylophone)
- Filtered envelope percussion (Handclaps, Shakers & Kick)
Produces a broadcast-grade, ultra-friendly 116 BPM preschool backing track.
"""

import math
import random
import struct
import wave
from pathlib import Path

def create_plucked_string(freq, duration, sample_rate=44100, damping=0.985, brightness=0.7):
    """Karplus-Strong acoustic plucked string synthesis."""
    n_samples = int(duration * sample_rate)
    delay_len = max(2, int(sample_rate / freq))
    # Initial noise burst with brightness control
    buffer = [random.uniform(-1.0, 1.0) * brightness for _ in range(delay_len)]
    
    samples = []
    idx = 0
    prev_sample = 0.0
    for _ in range(n_samples):
        # Averaging filter creates authentic string decay
        val = (buffer[idx] + prev_sample) * 0.5 * damping
        prev_sample = buffer[idx]
        buffer[idx] = val
        idx = (idx + 1) % delay_len
        samples.append(val)
    return samples

def create_bell_note(freq, duration, sample_rate=44100):
    """Modal glockenspiel / bell synthesis."""
    n_samples = int(duration * sample_rate)
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        # Fundamentals and non-harmonic metallic overtones
        env1 = math.exp(-t * 5.0)
        env2 = math.exp(-t * 9.0)
        env3 = math.exp(-t * 14.0)
        v = (
            0.6 * math.sin(2 * math.pi * freq * t) * env1 +
            0.3 * math.sin(2 * math.pi * freq * 2.76 * t) * env2 +
            0.15 * math.sin(2 * math.pi * freq * 5.40 * t) * env3
        )
        samples.append(v)
    return samples

def create_shaker(duration, sample_rate=44100):
    """Acoustic sand shaker."""
    n_samples = int(duration * sample_rate)
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration)) ** 2
        noise = random.uniform(-1.0, 1.0) * env * 0.25
        samples.append(noise)
    return samples

def create_handclap(duration=0.12, sample_rate=44100):
    """Crisp preschool handclap."""
    n_samples = int(duration * sample_rate)
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        env = math.exp(-t * 32.0)
        # Multi-burst clap
        burst = 1.0
        if t < 0.012:
            burst = 0.6
        elif t < 0.024:
            burst = 0.8
        samples.append(random.uniform(-1.0, 1.0) * env * burst * 0.5)
    return samples

def generate_preschool_soundtrack(output_path, total_duration=48.0, bpm=116, sample_rate=44100):
    """
    Arranges a joyful, bouncy preschool nursery rhyme track in C Major:
    Chords: C -> G -> Am -> F (The classic feel-good kids progression)
    """
    beat_dur = 60.0 / bpm # ~0.517s
    n_total_samples = int(total_duration * sample_rate)
    master_mix = [0.0] * n_total_samples

    # C Major chord notes (Ukulele voicings)
    chord_progression = [
        # C Major: C4, E4, G4, C5
        [261.63, 329.63, 392.00, 523.25],
        # G Major: G3, D4, G4, B4
        [196.00, 293.66, 392.00, 493.88],
        # A Minor: A3, E4, A4, C5
        [220.00, 329.63, 440.00, 523.25],
        # F Major: F3, C4, F4, A4
        [174.61, 261.63, 349.23, 440.00]
    ]
    bass_notes = [130.81, 98.00, 110.00, 87.31] # C3, G2, A2, F2

    # Glockenspiel nursery melody motif
    melody_motif = [
        (523.25, 0.5), (587.33, 0.5), (659.25, 1.0), # C5, D5, E5
        (587.33, 0.5), (523.25, 0.5), (392.00, 1.0), # D5, C5, G4
        (440.00, 0.5), (523.25, 0.5), (587.33, 1.0), # A4, C5, D5
        (523.25, 2.0)                                 # C5 hold
    ]

    # Render loop
    current_time = 0.0
    bar_idx = 0
    while current_time < total_duration:
        chord = chord_progression[bar_idx % len(chord_progression)]
        bass_freq = bass_notes[bar_idx % len(bass_notes)]
        
        # 1. Bouncy Bass on Beats 1 and 3
        for beat_offset in [0, 2]:
            b_time = current_time + (beat_offset * beat_dur)
            if b_time + 0.6 < total_duration:
                bass_wave = create_plucked_string(bass_freq, duration=beat_dur * 1.5, sample_rate=sample_rate, damping=0.992)
                start_s = int(b_time * sample_rate)
                for s_i, s_v in enumerate(bass_wave):
                    if start_s + s_i < n_total_samples:
                        master_mix[start_s + s_i] += s_v * 0.40

        # 2. Strummed Ukulele on all 4 beats (Down, Down-Up, Down, Down-Up)
        for beat in range(4):
            strum_time = current_time + (beat * beat_dur)
            # Down strum
            for note_i, freq in enumerate(chord):
                strum_wave = create_plucked_string(freq, duration=beat_dur * 0.9, sample_rate=sample_rate, damping=0.980)
                # Slight micro-arpeggio across strings
                start_s = int((strum_time + note_i * 0.012) * sample_rate)
                for s_i, s_v in enumerate(strum_wave):
                    if start_s + s_i < n_total_samples:
                        master_mix[start_s + s_i] += s_v * 0.16
            
            # Up strum on '&' of beat 2 and 4
            if beat in (1, 3):
                up_time = strum_time + (beat_dur * 0.5)
                for note_i, freq in enumerate(reversed(chord)):
                    up_wave = create_plucked_string(freq, duration=beat_dur * 0.5, sample_rate=sample_rate, damping=0.975)
                    start_s = int((up_time + note_i * 0.008) * sample_rate)
                    for s_i, s_v in enumerate(up_wave):
                        if start_s + s_i < n_total_samples:
                            master_mix[start_s + s_i] += s_v * 0.12

        # 3. Handclaps on Beats 2 and 4
        for beat in [1, 3]:
            clap_time = current_time + (beat * beat_dur)
            clap_wave = create_handclap(sample_rate=sample_rate)
            start_s = int(clap_time * sample_rate)
            for s_i, s_v in enumerate(clap_wave):
                if start_s + s_i < n_total_samples:
                    master_mix[start_s + s_i] += s_v * 0.32

        # 4. Shakers on every eighth note
        for eighth in range(8):
            shk_time = current_time + (eighth * (beat_dur * 0.5))
            shk_wave = create_shaker(duration=0.15, sample_rate=sample_rate)
            start_s = int(shk_time * sample_rate)
            for s_i, s_v in enumerate(shk_wave):
                if start_s + s_i < n_total_samples:
                    master_mix[start_s + s_i] += s_v * 0.22

        # 5. Glockenspiel Melody Note
        note_cursor = 0.0
        for m_freq, m_dur_beats in melody_motif:
            mel_time = current_time + (note_cursor * beat_dur)
            if mel_time + 0.4 < total_duration:
                bell_wave = create_bell_note(m_freq, duration=m_dur_beats * beat_dur * 1.2, sample_rate=sample_rate)
                start_s = int(mel_time * sample_rate)
                for s_i, s_v in enumerate(bell_wave):
                    if start_s + s_i < n_total_samples:
                        master_mix[start_s + s_i] += s_v * 0.28
            note_cursor += m_dur_beats

        current_time += 4 * beat_dur
        bar_idx += 1

    # Soft fade-out in last 2 seconds
    fade_samples = int(2.0 * sample_rate)
    start_fade = n_total_samples - fade_samples
    for i in range(fade_samples):
        vol = (fade_samples - i) / fade_samples
        master_mix[start_fade + i] *= vol

    # Peak normalization to -1.5 dB (0.84)
    max_val = max(abs(s) for s in master_mix) or 1.0
    scale = 0.84 / max_val
    pcm_data = bytearray()
    for s in master_mix:
        val = int(max(-32767, min(32767, s * scale * 32767)))
        pcm_data.extend(struct.pack('<h', val))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data)

    print(f"🎶 Successfully created acoustic nursery preschool soundtrack: {output_path.name} ({total_duration:.1f}s)")
    return output_path

if __name__ == "__main__":
    generate_preschool_soundtrack("test_acoustic_nursery.wav", total_duration=10.0)
