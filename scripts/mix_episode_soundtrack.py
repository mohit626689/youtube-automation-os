#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path

def mix_episode(ep_dir):
    ep_dir = Path(ep_dir).resolve()
    with open(ep_dir / "voice_timeline.json") as f:
        voice_segs = json.load(f)

    total_dur = round(voice_segs[-1]["end"] + 2.2, 2)

    inputs = ["-stream_loop", "-1", "-i", str(ep_dir / "preview_melody.wav")]
    filter_parts = [f"[0:a]volume=0.20,afade=t=out:st={total_dur - 1.8:.2f}:d=1.8[bg];"]
    mix_sources = ["[bg]"]

    # Add 8 voice segments
    for i, seg in enumerate(voice_segs):
        inputs.extend(["-i", seg["wav_path"]])
        inp_id = i + 1
        delay_ms = int(round(seg["start"] * 1000))
        filter_parts.append(f"[{inp_id}:a]adelay={delay_ms}|{delay_ms},volume=1.0[v{inp_id}];")
        mix_sources.append(f"[v{inp_id}]")

    cur_inp = len(voice_segs) + 1

    # SFX: 1. Pop at start (100ms)
    inputs.extend(["-i", str(ep_dir / "sfx_pop.wav")])
    filter_parts.append(f"[{cur_inp}:a]adelay=100|100,volume=0.75[sfx_pop];")
    mix_sources.append("[sfx_pop]")
    cur_inp += 1

    # SFX: 2. Splish Splash on "Splish, splash, rinse the soap" (Line 3 start)
    splash_delay = int(round(voice_segs[3]["start"] * 1000))
    inputs.extend(["-i", str(ep_dir / "sfx_splash.wav")])
    filter_parts.append(f"[{cur_inp}:a]adelay={splash_delay}|{splash_delay},volume=0.85[sfx_splash];")
    mix_sources.append("[sfx_splash]")
    cur_inp += 1

    # SFX: 3. Chime on bubble game (Line 5 start)
    chime_delay = int(round(voice_segs[5]["start"] * 1000))
    inputs.extend(["-i", str(ep_dir / "sfx_chime.wav")])
    filter_parts.append(f"[{cur_inp}:a]adelay={chime_delay}|{chime_delay},volume=0.8[sfx_chime];")
    mix_sources.append("[sfx_chime]")
    cur_inp += 1

    # SFX: 4. High five cheer on celebration (Line 6 start)
    cheer_delay = int(round(voice_segs[6]["start"] * 1000))
    inputs.extend(["-i", str(ep_dir / "sfx_cheer.wav")])
    filter_parts.append(f"[{cur_inp}:a]adelay={cheer_delay}|{cheer_delay},volume=0.85[sfx_cheer];")
    mix_sources.append("[sfx_cheer]")
    cur_inp += 1

    sources_str = "".join(mix_sources)
    filter_parts.append(f"{sources_str}amix=inputs={len(mix_sources)}:normalize=0:dropout_transition=2[outa]")

    out_audio = ep_dir / "soundtrack_with_vocals.wav"
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[outa]",
        "-t", f"{total_dur:.2f}",
        "-ar", "44100",
        "-c:a", "pcm_s16le",
        str(out_audio)
    ]
    subprocess.run(cmd, check=True)
    print("✅ Successfully mixed complete audio soundtrack:", out_audio.name, f"({total_dur}s)")

if __name__ == "__main__":
    ep = sys.argv[1] if len(sys.argv) > 1 else "episodes/Ep_030_Wash_Hands"
    mix_episode(ep)
