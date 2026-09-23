#!/usr/bin/env python3
"""
ABC Zoo TV — Automated Video Compositor (FFmpeg & ASS Engine)
Combines visual scene frames, background audio/music, and synced lyrics into
broadcast-ready 1080p 16:9 YouTube videos and 1080x1920 9:16 YouTube Shorts.

Features:
- Dynamic Ken Burns motion (smooth camera zooms and pans for each scene)
- Styled preschool bubble subtitles (thick dark outlines, bright primary colors)
- Dual format exports (16:9 Landscape & 9:16 Vertical Shorts)
- Automatic preview audio synthesis if external music file is not yet supplied
"""

import os
import sys
import math
import wave
import struct
import shutil
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def check_ffmpeg():
    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        raise RuntimeError("FFmpeg is not installed or not in PATH.")
    return ffmpeg_bin

def generate_preview_audio(output_path, duration_sec=30):
    """
    Synthesizes a cheerful, bouncy preschool marimba/xylophone preview melody
    in 112 BPM if no external audio file is provided.
    """
    sample_rate = 44100
    n_samples = int(sample_rate * duration_sec)
    
    # 112 BPM -> 0.535 seconds per beat
    beat_dur = 60.0 / 112.0
    
    # Simple C-Major Pentatonic notes for cheerful preschool melody: C4, D4, E4, G4, A4, C5
    notes = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25]
    melody_pattern = [0, 2, 3, 5, 3, 2, 1, 0, 2, 4, 5, 4, 3, 2, 0, 3]
    
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        beat_idx = int(t / (beat_dur / 2)) % len(melody_pattern)
        freq = notes[melody_pattern[beat_idx] % len(notes)]
        
        # Note envelope (decaying bell/marimba stroke)
        t_in_beat = (t % (beat_dur / 2))
        decay = math.exp(-t_in_beat * 7.0)
        
        # Fundamental tone + sparkle harmonic
        val = 0.5 * math.sin(2 * math.pi * freq * t) + 0.25 * math.sin(4 * math.pi * freq * t)
        val *= decay
        
        # Soft rhythmic bass pulse on downbeats
        t_in_full_beat = t % beat_dur
        bass_decay = math.exp(-t_in_full_beat * 9.0)
        bass_val = 0.3 * math.sin(2 * math.pi * 130.81 * t) * bass_decay
        
        mix = (val + bass_val) * 0.7
        # Clamp to 16-bit integer
        clamped = max(-1.0, min(1.0, mix))
        samples.append(int(clamped * 32767))
        
    with wave.open(str(output_path), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        raw_data = struct.pack(f"<{len(samples)}h", *samples)
        wav_file.writeframes(raw_data)
        
    print(f"🎵 Generated {duration_sec}s cheerful preview preschool audio track: {output_path.name}")
    return output_path

def srt_to_ass(srt_path, ass_path, video_width=1920, video_height=1080, is_shorts=False):
    """
    Converts standard SRT into an Advanced SubStation Alpha (.ass) file
    with customized high-contrast preschool typography and styling.
    """
    font_size = 64 if not is_shorts else 52
    outline = 7 if not is_shorts else 6
    margin_v = 110 if not is_shorts else 350
    
    # ASS Header with preschool style
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {video_width}
PlayResY: {video_height}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: PreschoolDefault,Arial Rounded MT Bold,{font_size},&H00FFFFFF,&H000000FF,&H004A151C,&H80000000,-1,0,0,0,100,100,1,0,1,{outline},3,2,60,60,{margin_v},1
Style: PhonicsHighlight,Arial Rounded MT Bold,{font_size + 4},&H0033E5FF,&H000000FF,&H004A151C,&H80000000,-1,0,0,0,105,105,1,0,1,{outline + 1},4,2,60,60,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    events = []
    if srt_path.exists():
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            
        blocks = content.split("\n\n")
        for b in blocks:
            lines = b.strip().split("\n")
            if len(lines) >= 3:
                times = lines[1].split(" --> ")
                start = times[0].strip().replace(",", ".")
                end = times[1].strip().replace(",", ".")
                
                # Format to ASS timestamp (H:MM:SS.cs)
                def fmt_time(t_str):
                    parts = t_str.split(":")
                    h = int(parts[0])
                    m = int(parts[1])
                    s_cs = parts[2]
                    # keep 2 decimal digits for centiseconds
                    s_parts = s_cs.split(".")
                    sec = int(s_parts[0])
                    cs = int(s_parts[1][:2]) if len(s_parts) > 1 else 0
                    return f"{h}:{m:02d}:{sec:02d}.{cs:02d}"
                
                start_ass = fmt_time(start)
                end_ass = fmt_time(end)
                text = " \\N ".join(lines[2:])
                
                # If text has letter mentions like "Letter A" or "Allie", use PhonicsHighlight style
                style = "PhonicsHighlight" if "Letter" in text or "/a/" in text else "PreschoolDefault"
                events.append(f"Dialogue: 0,{start_ass},{end_ass},{style},,0,0,0,,{text}")
                
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
        
    return ass_path

def build_video(episode_dir, output_format="landscape", custom_audio_path=None, target_duration=30):
    episode_dir = Path(episode_dir)
    if not episode_dir.exists():
        raise FileNotFoundError(f"Episode directory not found: {episode_dir}")
        
    ffmpeg_bin = check_ffmpeg()
    
    # 1. Discover scenes
    scenes = sorted(list(episode_dir.glob("scene_*.jpg")) + list(episode_dir.glob("scene_*.png")))
    if not scenes:
        # Fallback to thumbnail if no scene frames exist
        thumb = episode_dir / "thumbnail_hero.jpg"
        if thumb.exists():
            scenes = [thumb]
        else:
            raise FileNotFoundError(f"No scene images (scene_*.jpg) found in {episode_dir}")
            
    print(f"🎬 Found {len(scenes)} visual scene frames for episode {episode_dir.name}")
    
    # 2. Audio preparation
    audio_path = custom_audio_path
    if not audio_path or not Path(audio_path).exists():
        # Check if song.mp3 or song.wav exists in episode directory
        local_song = list(episode_dir.glob("*.mp3")) + list(episode_dir.glob("*.wav"))
        if local_song:
            audio_path = local_song[0]
            print(f"🎵 Using existing audio: {audio_path.name}")
        else:
            preview_audio = episode_dir / "preview_melody.wav"
            audio_path = generate_preview_audio(preview_audio, duration_sec=target_duration)
    else:
        audio_path = Path(audio_path)
        
    # 3. Subtitle styling (ASS)
    srt_files = list(episode_dir.glob("subtitles_*.srt"))
    ass_path = None
    if srt_files:
        srt_file = srt_files[0]
        ass_path = episode_dir / f"styled_subtitles_{output_format}.ass"
        is_shorts = (output_format == "shorts")
        w = 1080 if is_shorts else 1920
        h = 1920 if is_shorts else 1080
        srt_to_ass(srt_file, ass_path, video_width=w, video_height=h, is_shorts=is_shorts)
        print(f"📝 Compiled styled preschool subtitles: {ass_path.name}")
        
    # 4. Construct FFmpeg Assembly Command
    is_shorts = (output_format == "shorts")
    out_filename = f"final_episode_{output_format}.mp4"
    output_video = episode_dir / out_filename
    
    # Distribute duration equally across scenes
    scene_dur = max(3.0, target_duration / len(scenes))
    fps = 30
    
    inputs = []
    filter_complex_parts = []
    
    # Add each scene image as an input loop
    for i, sc in enumerate(scenes):
        inputs.extend(["-loop", "1", "-t", str(scene_dur), "-i", str(sc)])
        
        # Ken Burns slow zoom motion
        # Alternating zoom in and zoom out
        if i % 2 == 0:
            zoom_expr = f"zoom+0.001"
        else:
            zoom_expr = f"if(eq(on,0),1.15,zoom-0.001)"
            
        if not is_shorts:
            # 16:9 Landscape: 1920x1080
            filter_complex_parts.append(
                f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                f"zoompan=z='{zoom_expr}':d={int(scene_dur * fps)}:s=1920x1080:fps={fps}[v{i}];"
            )
        else:
            # 9:16 Shorts: 1080x1920
            filter_complex_parts.append(
                f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                f"zoompan=z='{zoom_expr}':d={int(scene_dur * fps)}:s=1080x1920:fps={fps}[v{i}];"
            )
            
    # Concatenate all visual scenes
    concat_inputs = "".join([f"[v{i}]" for i in range(len(scenes))])
    concat_filter = f"{concat_inputs}concat=n={len(scenes)}:v=1:a=0[vconcat];"
    filter_complex_parts.append(concat_filter)
    
    # Overlay subtitles if available
    final_v_label = "[vconcat]"
    if ass_path and ass_path.exists():
        # Escape path for FFmpeg subtitles filter
        ass_escaped = str(ass_path).replace("\\", "/").replace(":", "\\:")
        filter_complex_parts.append(f"[vconcat]ass='{ass_escaped}'[vsub];")
        final_v_label = "[vsub]"
        
    full_filter = "".join(filter_complex_parts)
    
    # Input audio index is at len(scenes)
    audio_idx = len(scenes)
    inputs.extend(["-i", str(audio_path)])
    
    cmd = [
        ffmpeg_bin,
        "-y",
        *inputs,
        "-filter_complex", full_filter,
        "-map", final_v_label,
        "-map", f"{audio_idx}:a",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_video)
    ]
    
    print(f"🚀 Running FFmpeg compositor for {output_format}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg Error:", res.stderr)
        raise RuntimeError(f"FFmpeg render failed: {res.stderr[-300:]}")
        
    file_size_mb = output_video.stat().st_size / (1024 * 1024)
    print(f"✅ Successfully exported {output_format.upper()} video: {output_video.name} ({file_size_mb:.2f} MB)")
    return output_video

def main():
    parser = argparse.ArgumentParser(description="ABC Zoo TV Automated Video Assembly")
    parser.add_argument("--episode_dir", type=str, default="episodes/Ep_001_Letter_A", help="Path to episode folder")
    parser.add_argument("--format", type=str, choices=["landscape", "shorts", "both"], default="both", help="Export format")
    parser.add_argument("--audio", type=str, default=None, help="Custom audio track (optional)")
    parser.add_argument("--duration", type=int, default=24, help="Target duration in seconds for preview")
    args = parser.parse_args()
    
    ep_path = BASE_DIR / args.episode_dir if not Path(args.episode_dir).is_absolute() else Path(args.episode_dir)
    
    if args.format in ["landscape", "both"]:
        build_video(ep_path, output_format="landscape", custom_audio_path=args.audio, target_duration=args.duration)
    if args.format in ["shorts", "both"]:
        build_video(ep_path, output_format="shorts", custom_audio_path=args.audio, target_duration=args.duration)

if __name__ == "__main__":
    main()
