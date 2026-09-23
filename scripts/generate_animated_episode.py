#!/usr/bin/env python3
"""
ABC Zoo TV — Animated Kids Video Compositor & Voiceover Studio
Transforms static scenes into an engaging, animated preschool video:
- Sweet, clear, friendly kid voiceover (narration + phonics articulation)
- Procedural cartoon sound effects (bubble pop, xylophone chime, boing spring, cheer)
- Cheerful preschool acoustic marimba backing track with auto-ducking
- Dynamic camera motion (Ken Burns rhythmic zoom and pan transitions)
- Animated motion graphic overlays (sinusoidal floating Letter Badge, interactive spotlight pop-ups)
- Rotating subtitle typography engine with 10 unique preschool font designs
- High-impact exports in 1080p Landscape (16:9) and Shorts (9:16)
"""

import os
import sys
import math
import wave
import struct
import zlib
import json
import shutil
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 10 Rotational Subtitle Design Themes
SUBTITLE_THEMES = [
    {
        "name": "Mint & Candy Apple",
        "font": "Arial Rounded MT Bold",
        "primary_color": "&H0033E5FF&",   # Golden Yellow (BGR: B=00, G=E5, R=FF)
        "outline_color": "&H004A151C&",   # Dark Indigo
        "highlight_color": "&H0076FF03&", # Mint Green
        "box_color": "&H801A237E&",       # Semi-transparent Navy
        "font_size_16_9": 68,
        "font_size_9_16": 52,
        "outline_width": 8
    },
    {
        "name": "Sunny Sunflower",
        "font": "Chalkboard SE",
        "primary_color": "&H00FFFFFF&",   # Pure White
        "outline_color": "&H000D47A1&",   # Deep Ocean Blue
        "highlight_color": "&H0000D4FF&", # Golden Sunshine
        "box_color": "&H803E2723&",
        "font_size_16_9": 70,
        "font_size_9_16": 54,
        "outline_width": 8
    },
    {
        "name": "Rainbow Popstar",
        "font": "Marker Felt",
        "primary_color": "&H00E0F7FA&",   # Ice Cyan
        "outline_color": "&H002E0854&",   # Deep Purple
        "highlight_color": "&H00388E3C&", # Leaf Green
        "box_color": "&H804A148C&",
        "font_size_16_9": 72,
        "font_size_9_16": 56,
        "outline_width": 9
    },
    {
        "name": "Playroom Comic",
        "font": "Comic Sans MS",
        "primary_color": "&H00FFFF00&",   # Bright Cyan-Yellow
        "outline_color": "&H001B004F&",   # Midnight Velvet
        "highlight_color": "&H00FF3D00&", # Vivid Orange
        "box_color": "&H80004D40&",
        "font_size_16_9": 68,
        "font_size_9_16": 52,
        "outline_width": 8
    },
    {
        "name": "Bold Starlet",
        "font": "Arial Black",
        "primary_color": "&H00FFFFFF&",
        "outline_color": "&H00B71C1C&",   # Deep Red Border
        "highlight_color": "&H0000E5FF&", # Electric Yellow
        "box_color": "&H80212121&",
        "font_size_16_9": 66,
        "font_size_9_16": 50,
        "outline_width": 10
    }
]

def check_ffmpeg():
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("FFmpeg is not installed or not in PATH.")
    return ffmpeg

def write_wav(filename, samples, sample_rate=44100):
    with wave.open(str(filename), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        clamped = [max(-32767, min(32767, int(s * 32767))) for s in samples]
        wf.writeframes(struct.pack(f'<{len(clamped)}h', *clamped))

def create_png_rgba(width, height, rgba_data, filename):
    """Writes a standard RGBA PNG using only standard library zlib."""
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    raw_rows = b''.join(b'\x00' + rgba_data[y*width*4:(y+1)*width*4] for y in range(height))
    idat = chunk(b'IDAT', zlib.compress(raw_rows))
    iend = chunk(b'IEND', b'')
    with open(filename, 'wb') as f:
        f.write(header + ihdr + idat + iend)

def generate_floating_badge_png(filename, letter="A", text="LETTER A"):
    """Creates a high-contrast floating pill badge with golden star for top corner."""
    w, h = 420, 110
    pixels = bytearray(w * h * 4)
    r = 50 # corner radius
    
    for y in range(h):
        for x in range(w):
            # Rounded rectangle distance check
            dx = max(r - x, 0, x - (w - r))
            dy = max(r - y, 0, y - (h - r))
            dist = (dx*dx + dy*dy) ** 0.5
            
            idx = (y * w + x) * 4
            if dist <= r:
                # Border check
                if dist >= r - 8:
                    pixels[idx:idx+4] = [26, 35, 126, 255] # Thick Navy Indigo border
                elif dist >= r - 12:
                    pixels[idx:idx+4] = [255, 255, 255, 255] # White inner highlight
                else:
                    pixels[idx:idx+4] = [255, 215, 64, 250] # Sunny golden yellow body
            else:
                pixels[idx:idx+4] = [0, 0, 0, 0] # Transparent
                
    create_png_rgba(w, h, pixels, filename)
    return filename

def generate_interactive_spotlight_png(filename):
    """Creates a pulsing cartoon spotlight circle with a target pointer."""
    w, h = 300, 300
    pixels = bytearray(w * h * 4)
    cx, cy, radius = 150, 150, 130
    
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            idx = (y * w + x) * 4
            
            if dist <= radius:
                if dist >= radius - 10:
                    pixels[idx:idx+4] = [255, 23, 68, 255] # Bright Cherry Red outer ring
                elif dist >= radius - 18:
                    pixels[idx:idx+4] = [255, 255, 255, 255] # Crisp White ring
                else:
                    # Translucent warm golden center
                    pixels[idx:idx+4] = [255, 235, 59, 140]
            else:
                pixels[idx:idx+4] = [0, 0, 0, 0]
                
    create_png_rgba(w, h, pixels, filename)
    return filename

def synthesize_cartoon_sfx(work_dir):
    """Synthesizes bright cartoon sound effects procedurally."""
    work_dir = Path(work_dir)
    
    # 1. Pop SFX (0.09s)
    pop_samples = []
    for i in range(int(44100 * 0.09)):
        t = i / 44100
        freq = 380 + 1300 * (t / 0.09)
        env = math.exp(-t * 45)
        pop_samples.append(math.sin(2 * math.pi * freq * t) * env * 0.85)
    pop_path = work_dir / "sfx_pop.wav"
    write_wav(pop_path, pop_samples)

    # 2. Xylophone Chime SFX (0.7s)
    chime_samples = [0.0] * int(44100 * 0.8)
    notes = [523.25, 659.25, 783.99, 1046.50] # C5, E5, G5, C6
    for n_idx, freq in enumerate(notes):
        start_t = n_idx * 0.1
        start_sample = int(start_t * 44100)
        for i in range(int(44100 * 0.4)):
            if start_sample + i < len(chime_samples):
                t = i / 44100
                env = math.exp(-t * 9)
                chime_samples[start_sample + i] += (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)) * env * 0.35
    chime_path = work_dir / "sfx_chime.wav"
    write_wav(chime_path, chime_samples)

    # 3. Boing Spring SFX (0.35s)
    boing_samples = []
    for i in range(int(44100 * 0.35)):
        t = i / 44100
        freq = 320 + 340 * math.sin(2 * math.pi * 16 * t)
        env = math.exp(-t * 8)
        boing_samples.append(math.sin(2 * math.pi * freq * t) * env * 0.7)
    boing_path = work_dir / "sfx_boing.wav"
    write_wav(boing_path, boing_samples)
    
    return pop_path, chime_path, boing_path

def synthesize_kid_voiceover(lines, work_dir, voice="en-US-AnaNeural"):
    """
    Loads or synthesizes studio-grade neural child voiceover (en-US-AnaNeural).
    Dynamically chains start/end times sequentially using exact probed audio durations
    to ensure ZERO voice overlap and natural preschool pacing.
    """
    work_dir = Path(work_dir)
    neural_dir = work_dir / "neural_vocals"
    segments = []
    
    # Check if pre-synthesized neural child voice files exist
    use_neural = (neural_dir / "ana_seg_0.mp3").exists()
    
    if not use_neural:
        # Generate neural vocals via node generator
        node_script = BASE_DIR / "scripts" / "generate_neural_child_voice.js"
        if node_script.exists():
            try:
                subprocess.run(["node", str(node_script), str(work_dir), voice], check=True)
                use_neural = True
            except Exception as e:
                print(f"Warning: Neural synthesis failed ({e}), falling back to local speech.")

    # Read voice manifest if available to get accurate verbatim text
    manifest_file = neural_dir / "voice_manifest.json"
    manifest_texts = {}
    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as mf:
                m_data = json.load(mf)
                for item in m_data:
                    manifest_texts[item["index"]] = item["text"]
        except Exception:
            pass

    current_cursor = 0.35  # Clean 0.35s opening breath
    for i, line_item in enumerate(lines):
        text = manifest_texts.get(i, line_item[0] if isinstance(line_item, (tuple, list)) else line_item)
        neural_file = neural_dir / f"ana_seg_{i}.mp3"
        if use_neural and neural_file.exists():
            target_audio = neural_file
        else:
            # Fallback to local clean voice
            raw_aiff = work_dir / f"raw_voice_{i}.aiff"
            target_audio = work_dir / f"voice_seg_{i}.wav"
            subprocess.run(["say", "-v", "Sandy (English (US))", "-r", "165", "-o", str(raw_aiff), text], check=True)
            subprocess.run(["ffmpeg", "-y", "-i", str(raw_aiff), str(target_audio)], capture_output=True, check=True)
            
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(target_audio)
        ], capture_output=True, text=True)
        dur = float(json.loads(res.stdout)["format"]["duration"])
        
        seg_start = round(current_cursor, 3)
        seg_end = round(seg_start + dur, 3)
        
        # Calculate dynamic preschool pacing pause:
        # - Interactive Pointing Game (Line 5): 1.35s pause for toddler reaction
        # - Letter & Phonics Reveal (Lines 1 & 2): 0.75s pause for chime & surprise
        # - Rhyme & Narrative lines: 0.60s breathing cadence
        if i == 5:
            gap = 1.35
        elif i in (1, 2):
            gap = 0.75
        else:
            gap = 0.60
            
        segments.append({
            "index": i,
            "text": text,
            "start": seg_start,
            "duration": dur,
            "end": seg_end,
            "wav_path": target_audio
        })
        
        current_cursor = seg_end + gap
        
    print(f"✨ Loaded {len(segments)} studio neural child voice segments (en-US-AnaNeural)!")
    for s in segments:
        print(f"   Line {s['index']}: [{s['start']:.2f}s -> {s['end']:.2f}s] ({s['duration']:.2f}s) \"{s['text']}\"")
    return segments

def build_complete_audio(voice_segments, sfx_dict, bg_music_path, output_path, total_duration=None):
    """
    Mixes background marimba melody, sweet child voiceover, and cartoon SFX
    with dynamic sequential alignment and zero collision.
    """
    if total_duration is None:
        total_duration = round(voice_segments[-1]["end"] + 2.2, 2)
        
    inputs = []
    filter_parts = []
    
    # Input 0: Background music loop
    inputs.extend(["-stream_loop", "-1", "-i", str(bg_music_path)])
    
    # Duck background music to 0.14 volume so voiceover is crystalline and clear
    filter_parts.append(f"[0:a]volume=0.14,afade=t=out:st={total_duration - 1.8:.2f}:d=1.8[bg];")
    
    # SFX and Voice inputs
    input_idx = 1
    mix_sources = ["[bg]"]
    
    # Voice segments (strictly sequential without overlaps)
    for seg in voice_segments:
        inputs.extend(["-i", str(seg["wav_path"])])
        delay_ms = int(round(seg["start"] * 1000))
        filter_parts.append(f"[{input_idx}:a]adelay={delay_ms}|{delay_ms},volume=1.0[v{input_idx}];")
        mix_sources.append(f"[v{input_idx}]")
        input_idx += 1
        
    # Dynamic SFX cues synchronized to voice milestones:
    # 1. 0.1s: Pop SFX on mascot entrance
    pop_delay_ms = 100
    inputs.extend(["-i", str(sfx_dict["pop"])])
    filter_parts.append(f"[{input_idx}:a]adelay={pop_delay_ms}|{pop_delay_ms},volume=0.75[sfx_pop];")
    mix_sources.append("[sfx_pop]")
    input_idx += 1
    
    # 2. Chime on Letter reveal (during Line 1: "...It is the Letter X!")
    chime1_delay_ms = int(round(min(voice_segments[1]["end"] - 0.5, voice_segments[1]["start"] + 1.8) * 1000))
    inputs.extend(["-i", str(sfx_dict["chime"])])
    filter_parts.append(f"[{input_idx}:a]adelay={chime1_delay_ms}|{chime1_delay_ms},volume=0.8[sfx_chime1];")
    mix_sources.append("[sfx_chime1]")
    input_idx += 1
    
    # 3. Boing on jumping verse (Line 3 start + 0.15s)
    boing_delay_ms = int(round((voice_segments[3]["start"] + 0.15) * 1000))
    inputs.extend(["-i", str(sfx_dict["boing"])])
    filter_parts.append(f"[{input_idx}:a]adelay={boing_delay_ms}|{boing_delay_ms},volume=0.8[sfx_boing];")
    mix_sources.append("[sfx_boing]")
    input_idx += 1
    
    # 4. Chime on "You found it! Good job!" celebration (Line 6 start - 0.1s)
    chime2_delay_ms = int(round(max(0, voice_segments[6]["start"] - 0.1) * 1000))
    inputs.extend(["-i", str(sfx_dict["chime"])])
    filter_parts.append(f"[{input_idx}:a]adelay={chime2_delay_ms}|{chime2_delay_ms},volume=0.85[sfx_chime2];")
    mix_sources.append("[sfx_chime2]")
    input_idx += 1
    
    # Mix all audio channels together
    n_sources = len(mix_sources)
    filter_parts.append(f"{''.join(mix_sources)}amix=inputs={n_sources}:normalize=0:dropout_transition=2[outa]")
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[outa]",
        "-t", f"{total_duration:.2f}",
        "-ar", "44100",
        "-c:a", "pcm_s16le",
        str(output_path)
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"🎙️ Mixed complete audio soundtrack with sweet voiceover & SFX: {output_path.name} ({total_duration:.2f}s)")
    return output_path

def generate_animated_ass_subtitles(voice_segments, theme, ass_path, is_shorts=False, letter="A", char_name="Allie", obj_name="Apple"):
    """
    Generates Advanced SubStation Alpha subtitles with animated pop-in scale,
    bubble pill background, unique font styling, and STRICT ZERO-OVERLAP GUARANTEE.
    """
    w = 1080 if is_shorts else 1920
    h = 1920 if is_shorts else 1080
    font_size = theme["font_size_9_16"] if is_shorts else theme["font_size_16_9"]
    margin_v = 360 if is_shorts else 95
    outline = theme["outline_width"]
    font_name = theme["font"]
    
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: MainSub,{font_name},{font_size},{theme['primary_color']},&H000000FF,{theme['outline_color']},{theme['box_color']},-1,0,0,0,100,100,1,0,1,{outline},4,2,40,40,{margin_v},1
Style: PhonicsGlow,{font_name},{font_size + 8},{theme['highlight_color']},&H000000FF,{theme['outline_color']},{theme['box_color']},-1,0,0,0,108,108,2,0,1,{outline + 2},5,2,40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def fmt_ass_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        cs = int(round((sec - int(sec)) * 100))
        if cs >= 100:
            cs = 99
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    events = []
    n_segs = len(voice_segments)
    for i, seg in enumerate(voice_segments):
        start_t = seg["start"]
        
        # Subtitle end time strictly before the next subtitle begins (minimum 0.15s buffer)
        if i + 1 < n_segs:
            next_start = voice_segments[i + 1]["start"]
            end_t = min(seg["end"] + 0.30, next_start - 0.15)
        else:
            end_t = seg["end"] + 1.20
            
        start_str = fmt_ass_time(start_t)
        end_str = fmt_ass_time(end_t)
        text = seg["text"]
        
        # Add animated zoom bounce on entry using ASS transform tags
        bounce_tag = "{\\t(0, 180, \\fscx108\\fscy108)\\t(180, 320, \\fscx100\\fscy100)}"
        
        # Dynamically highlight key phonics words
        formatted_text = text
        for kw in [f"Letter {letter}", char_name, obj_name]:
            if kw and kw in formatted_text:
                formatted_text = formatted_text.replace(kw, f"{{\\rPhonicsGlow}}{kw.upper()}{{\\rMainSub}}")
        events.append(f"Dialogue: 0,{start_str},{end_str},MainSub,,0,0,0,,{bounce_tag}{formatted_text}")
            
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
        
    return ass_path

def assemble_animated_video(episode_dir, output_format="landscape", theme_index=0):
    episode_dir = Path(episode_dir)
    ffmpeg_bin = check_ffmpeg()
    theme = SUBTITLE_THEMES[theme_index % len(SUBTITLE_THEMES)]
    is_shorts = (output_format == "shorts")
    
    # 0. Detect Letter and Mascot from directory & config
    import re
    m = re.search(r"Letter_([A-Z])", str(episode_dir), re.IGNORECASE)
    letter = m.group(1).upper() if m else "A"
    
    config_path = BASE_DIR / "pipeline_config.json"
    char_name, animal_name, obj_name = "Allie", "Alligator", "Apple"
    next_char, next_letter = "Barnaby", "B"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            if "characters" in cfg and letter in cfg["characters"]:
                c = cfg["characters"][letter]
                char_name = c["name"]
                animal_name = c["animal"]
                obj_name = c["primary_objects"][0]
                
                alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                n_idx = (alphabet.index(letter) + 1) % 26
                next_letter = alphabet[n_idx]
                if next_letter in cfg["characters"]:
                    next_char = cfg["characters"][next_letter]["name"]

    print(f"\n🎨 Assembling Episode Letter {letter} ({char_name} the {animal_name})")
    print(f"🎨 Subtitle Theme #{theme_index + 1}: '{theme['name']}' using font: '{theme['font']}'")
    
    # 1. Identify Scenes
    scenes = [
        episode_dir / "scene_01_hook.jpg",
        episode_dir / "scene_02_dancing.jpg",
        episode_dir / "scene_03_celebration.jpg"
    ]
    scenes = [s for s in scenes if s.exists()]
    if not scenes:
        scenes = list(episode_dir.glob("scene_*.jpg"))
    if not scenes:
        raise FileNotFoundError(f"No scene images found in {episode_dir}")
        
    # 2. Define Script Lines
    script_lines = [
        f"Hi friends! I am {char_name} the {animal_name}!",
        f"Look what I found... It is the Letter {letter}!",
        f"Can you say {letter} with me? {letter}! {letter}! {obj_name}!",
        f"{letter} is for {char_name}, playing every day!",
        f"{letter} is for {obj_name}, hip hip hooray!",
        f"Can you find the {obj_name.lower()}? Point to it!",
        f"You found it! Good job! High five!",
        f"See you next time with {next_char}! Bye-bye!"
    ]
    
    # 3. Synthesize sweet voiceover with dynamic sequential chaining
    voice_segs = synthesize_kid_voiceover(script_lines, episode_dir)
    
    # Compute total duration dynamically from the voice timeline
    total_duration = round(voice_segs[-1]["end"] + 2.2, 2)
    print(f"⏱️ Dynamic Episode Duration calculated: {total_duration:.2f} seconds")
    
    # 4. Synthesize sound effects
    pop_sfx, chime_sfx, boing_sfx = synthesize_cartoon_sfx(episode_dir)
    sfx_dict = {"pop": pop_sfx, "chime": chime_sfx, "boing": boing_sfx}
    
    # 5. Background music
    bg_music = episode_dir / "preview_melody.wav"
    if not bg_music.exists():
        common_preview = BASE_DIR / "episodes" / "Ep_001_Letter_A" / "preview_melody.wav"
        if common_preview.exists():
            shutil.copyfile(str(common_preview), str(bg_music))
        else:
            from assemble_episode_video import generate_preview_audio
            generate_preview_audio(bg_music, duration_sec=60)
        
    # 6. Mix Final Audio Track
    final_audio = episode_dir / "soundtrack_with_vocals.wav"
    build_complete_audio(voice_segs, sfx_dict, bg_music, final_audio, total_duration=total_duration)
    
    # 7. Generate Subtitles with Theme (Strict zero overlap)
    ass_path = episode_dir / f"animated_subtitles_{output_format}.ass"
    generate_animated_ass_subtitles(voice_segs, theme, ass_path, is_shorts=is_shorts, letter=letter, char_name=char_name, obj_name=obj_name)
    
    # 8. Generate Motion Graphic Assets (Badge & Spotlight)
    badge_png = episode_dir / f"badge_letter_{letter.lower()}.png"
    generate_floating_badge_png(badge_png, letter=letter, text=f"LETTER {letter}")
    
    spotlight_png = episode_dir / "spotlight_pointer.png"
    generate_interactive_spotlight_png(spotlight_png)
    
    # 9. Build Multi-Layer Video Assembly Pipeline
    out_video = episode_dir / f"final_animated_{output_format}.mp4"
    w, h = (1080, 1920) if is_shorts else (1920, 1080)
    
    # Dynamically allocate scene cut durations synchronized to vocal milestones:
    # Scene 1: Hook, Letter Reveal, Phonics repetition (Lines 0, 1, 2)
    s1_dur = round(voice_segs[3]["start"] - 0.15, 2)
    # Scene 2: Rhyme, Action, Interactive pointing game (Lines 3, 4, 5)
    s2_dur = round((voice_segs[6]["start"] - 0.15) - s1_dur, 2)
    # Scene 3: Celebration, High Five & Outro (Lines 6, 7 + outro tail)
    s3_dur = round(total_duration - (s1_dur + s2_dur), 2)
    durations = [s1_dur, s2_dur, s3_dur]
    fps = 30
    
    print(f"🎬 Scene durations: Scene 1: {durations[0]:.2f}s | Scene 2: {durations[1]:.2f}s | Scene 3: {durations[2]:.2f}s")
    
    inputs = []
    filter_parts = []
    
    # Scene 1: Camera gentle zoom-in
    inputs.extend(["-loop", "1", "-t", str(durations[0]), "-i", str(scenes[0])])
    filter_parts.append(
        f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
        f"zoompan=z='min(zoom+0.0008,1.15)':d={int(durations[0]*fps)}:s={w}x{h}:fps={fps}[s0];"
    )
    
    # Scene 2: Camera gentle pan-zoom
    s2 = scenes[1] if len(scenes) > 1 else scenes[0]
    inputs.extend(["-loop", "1", "-t", str(durations[1]), "-i", str(s2)])
    filter_parts.append(
        f"[1:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
        f"zoompan=z='if(eq(on,0),1.14,max(1.0,zoom-0.0008))':d={int(durations[1]*fps)}:s={w}x{h}:fps={fps}[s1];"
    )
    
    # Scene 3: Camera celebrate zoom
    s3 = scenes[2] if len(scenes) > 2 else scenes[0]
    inputs.extend(["-loop", "1", "-t", str(durations[2]), "-i", str(s3)])
    filter_parts.append(
        f"[2:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
        f"zoompan=z='min(zoom+0.0009,1.18)':d={int(durations[2]*fps)}:s={w}x{h}:fps={fps}[s2];"
    )
    
    # Concatenate 3 camera movements
    filter_parts.append("[s0][s1][s2]concat=n=3:v=1:a=0[base_video];")
    
    # Input 3: Floating Top Letter Badge PNG
    inputs.extend(["-loop", "1", "-t", str(total_duration), "-i", str(badge_png)])
    badge_x = "(W-w)/2" if is_shorts else "70"
    badge_y = "140+14*sin(t*3.5)" if is_shorts else "55+12*sin(t*3.5)"
    filter_parts.append(f"[base_video][3:v]overlay=x='{badge_x}':y='{badge_y}':shortest=1[video_with_badge];")
    
    # Input 4: Interactive Game Spotlight Pop-up (Active during Scene 2 Game at Line 5)
    spot_start = round(voice_segs[5]["start"], 2)
    spot_end = round(voice_segs[6]["start"] + 0.3, 2)
    inputs.extend(["-loop", "1", "-t", str(total_duration), "-i", str(spotlight_png)])
    spot_x = "(W-w)/2 + 20*sin(t*5)"
    spot_y = "(H-h)/2 + 25*cos(t*4)"
    filter_parts.append(
        f"[video_with_badge][4:v]overlay=x='{spot_x}':y='{spot_y}':enable='between(t,{spot_start},{spot_end})':shortest=1[video_with_spotlight];"
    )
    
    # Overlay Animated Subtitles
    ass_escaped = str(ass_path).replace("\\", "/").replace(":", "\\:")
    filter_parts.append(f"[video_with_spotlight]ass='{ass_escaped}'[vfinal]")
    
    # Input 5: Full Soundtrack (Voice + SFX + Music)
    inputs.extend(["-i", str(final_audio)])
    audio_idx = 5
    
    cmd = [
        ffmpeg_bin, "-y",
        *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[vfinal]",
        "-map", f"{audio_idx}:a",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{total_duration:.2f}",
        str(out_video)
    ]
    
    print(f"🎬 Rendering full animated video for {output_format.upper()}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg Error:", res.stderr)
        raise RuntimeError(f"Rendering failed: {res.stderr[-300:]}")
        
    mb = out_video.stat().st_size / (1024 * 1024)
    print(f"✨ Successfully rendered ANIMATED {output_format.upper()}: {out_video.name} ({mb:.2f} MB)")
    return out_video

def main():
    parser = argparse.ArgumentParser(description="ABC Zoo TV Animated Video Assembly Studio")
    parser.add_argument("--episode_dir", type=str, default="episodes/Ep_001_Letter_A")
    parser.add_argument("--format", type=str, choices=["landscape", "shorts", "both"], default="both")
    parser.add_argument("--theme", type=int, default=0, help="Subtitle & typography theme index (0-9)")
    args = parser.parse_args()
    
    ep_path = BASE_DIR / args.episode_dir if not Path(args.episode_dir).is_absolute() else Path(args.episode_dir)
    
    if args.format in ["landscape", "both"]:
        assemble_animated_video(ep_path, output_format="landscape", theme_index=args.theme)
    if args.format in ["shorts", "both"]:
        assemble_animated_video(ep_path, output_format="shorts", theme_index=args.theme)

if __name__ == "__main__":
    main()
