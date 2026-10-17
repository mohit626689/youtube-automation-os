#!/usr/bin/env python3
"""
HyperFrames Video Compositor for ABC Zoo TV & Universal YouTube Automation
Renders 60fps butter-smooth animations, kinetic typography, and fluid camera motion
using HTML/CSS/GSAP and HyperFrames.
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def check_hyperframes():
    local_bin = BASE_DIR / "node_modules" / ".bin" / "hyperframes"
    if local_bin.exists():
        return str(local_bin)
    system_bin = shutil.which("hyperframes")
    if system_bin:
        return system_bin
    raise RuntimeError("HyperFrames CLI not found in node_modules or PATH.")

def get_accurate_voice_timeline(episode_dir):
    """
    Loads or dynamically probes the accurate audio timeline for voiceover segments,
    guaranteeing 100% synchronization between speech, subtitles, scene cuts, and game spotlights.
    """
    episode_dir = Path(episode_dir)
    timeline_file = episode_dir / "voice_timeline.json"
    if timeline_file.exists():
        try:
            with open(timeline_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if len(data) > 1 and data[1].get("start", 0) > 0 and data[0].get("end", 0) > 0:
                return data
        except Exception:
            pass

    neural_dir = episode_dir / "neural_vocals"
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

    lines_file = episode_dir / "lines.json"
    if lines_file.exists() and not manifest_texts:
        try:
            with open(lines_file, "r", encoding="utf-8") as lf:
                lines_data = json.load(lf)
                for idx, l in enumerate(lines_data):
                    manifest_texts[idx] = l if isinstance(l, str) else l.get("text", "")
        except Exception:
            pass

    audio_segs = sorted(list(neural_dir.glob("ana_seg_*.mp3")), key=lambda p: int(p.stem.split("_")[-1]))
    if not audio_segs:
        audio_segs = sorted(list(episode_dir.glob("voice_seg_*.wav")), key=lambda p: int(p.stem.split("_")[-1]))

    if not audio_segs:
        raise FileNotFoundError(f"No voice segment audio files found in {neural_dir} or {episode_dir}")

    ffprobe = shutil.which("ffprobe")
    segments = []
    current_cursor = 0.35  # Clean 0.35s opening breath
    for i, audio_path in enumerate(audio_segs):
        res = subprocess.run([
            ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "json", str(audio_path)
        ], capture_output=True, text=True, check=True)
        dur = float(json.loads(res.stdout)["format"]["duration"])
        text = manifest_texts.get(i, f"Line {i}")
        
        seg_start = round(current_cursor, 3)
        seg_end = round(seg_start + dur, 3)
        
        gap = 1.35 if i == 5 else (0.75 if i in (1, 2) else 0.60)
        segments.append({
            "index": i,
            "text": text,
            "start": seg_start,
            "duration": dur,
            "end": seg_end,
            "wav_path": str(audio_path)
        })
        current_cursor = seg_end + gap

    try:
        with open(timeline_file, "w", encoding="utf-8") as f:
            json.dump(segments, f, indent=2)
        print(f"💾 Saved calibrated voice timeline to {timeline_file.name}")
    except Exception:
        pass

    return segments

def generate_hyperframes_composition(episode_dir, output_format="shorts", theme_index=0):
    episode_dir = Path(episode_dir)
    is_shorts = (output_format == "shorts")
    w = 1080 if is_shorts else 1920
    h = 1920 if is_shorts else 1080
    
    # 1. Parse Letter and Character metadata
    import re
    m = re.search(r"Letter_([A-Z])", str(episode_dir), re.IGNORECASE)
    letter = m.group(1).upper() if m else "A"
    
    badge_text_file = episode_dir / "badge_text.txt"
    if badge_text_file.exists():
        badge_text = badge_text_file.read_text(encoding="utf-8").strip()
    else:
        badge_text = f"LETTER {letter}"
    
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

    # 2. Get Scenes
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
    
    # 3. Load accurate voice timeline with dynamic sequential timestamps
    voice_segs = get_accurate_voice_timeline(episode_dir)
        
    # Get audio file and total duration
    audio_file = episode_dir / "soundtrack_with_vocals.wav"
    if not audio_file.exists():
        raise FileNotFoundError(f"Soundtrack audio not found: {audio_file}")
        
    # Probe duration
    ffprobe = shutil.which("ffprobe")
    probe_res = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)],
        capture_output=True, text=True, check=True
    )
    total_duration = round(float(probe_res.stdout.strip()), 2)
    
    # Scene cut timing
    s1_dur = round(voice_segs[3]["start"] - 0.15, 2)
    s2_dur = round((voice_segs[6]["start"] - 0.15) - s1_dur, 2)
    s3_dur = round(total_duration - (s1_dur + s2_dur), 2)
    
    # Create project directory for HyperFrames
    hf_dir = episode_dir / f"hyperframes_{output_format}"
    hf_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy/Link assets into hf_dir
    shutil.copyfile(str(scenes[0]), str(hf_dir / "scene_01.jpg"))
    shutil.copyfile(str(scenes[0]), str(hf_dir / "amb_01.jpg"))
    s2 = scenes[1] if len(scenes) > 1 else scenes[0]
    shutil.copyfile(str(s2), str(hf_dir / "scene_02.jpg"))
    shutil.copyfile(str(s2), str(hf_dir / "amb_02.jpg"))
    s3 = scenes[2] if len(scenes) > 2 else scenes[0]
    shutil.copyfile(str(s3), str(hf_dir / "scene_03.jpg"))
    shutil.copyfile(str(s3), str(hf_dir / "amb_03.jpg"))
    
    badge_png = episode_dir / f"badge_letter_{letter.lower()}.png"
    if badge_png.exists():
        shutil.copyfile(str(badge_png), str(hf_dir / "badge.png"))
        
    spotlight_png = episode_dir / "spotlight_pointer.png"
    if spotlight_png.exists():
        shutil.copyfile(str(spotlight_png), str(hf_dir / "spotlight.png"))
        
    shutil.copyfile(str(audio_file), str(hf_dir / "soundtrack.wav"))
    
    # Write hyperframes.json
    hf_json = {
        "formatVersion": "1.0",
        "entry": "index.html",
        "fps": 60,
        "width": w,
        "height": h,
        "duration": total_duration
    }
    with open(hf_dir / "hyperframes.json", "w", encoding="utf-8") as f:
        json.dump(hf_json, f, indent=2)

    # Subtitle cues with highlights
    sub_elements_html = []
    sub_animations_js = []
    for i, seg in enumerate(voice_segs):
        st = round(seg["start"], 2)
        speech_end = round(seg.get("end", st + seg.get("duration", 3.0)), 2)
        next_st = round(voice_segs[i+1]["start"], 2) if i+1 < len(voice_segs) else total_duration - 0.4
        et = round(min(speech_end + 0.35, next_st - 0.10), 2)
        text = seg["text"]
        
        # Safe color highlight (word boundary only, avoiding HTML corruption)
        display_text = text
        for kw in [f"Letter {letter}", char_name, obj_name]:
            if kw and len(kw) > 1 and kw in display_text:
                display_text = re.sub(r'\b' + re.escape(kw) + r'\b', f'<span class="highlight">{kw}</span>', display_text)
                
        sub_elements_html.append(
            f'        <div id="sub-{i}" class="sub-pill">\n'
            f'          <div class="sub-inner">{display_text}</div>\n'
            f'        </div>'
        )
        
        fade_out_time = round(max(st + 0.3, et - 0.2), 2)
        sub_animations_js.append(
            f'      // Subtitle {i} (Speech: {st}s -> {speech_end}s, Display: {st}s -> {et}s)\n'
            f'      tl.fromTo("#sub-{i}", {{ opacity: 0, y: 15, scale: 0.88 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {st});\n'
            f'      tl.to("#sub-{i}", {{ opacity: 0, y: -10, duration: 0.2, ease: "power2.in" }}, {fade_out_time});'
        )

    spot_start = round(voice_segs[5]["start"], 2) if len(voice_segs) > 5 else round(total_duration * 0.6, 2)
    spot_end = round(voice_segs[6]["start"] + 0.25, 2) if len(voice_segs) > 6 else round(spot_start + 4.0, 2)
    badge_repeats = int(total_duration / 2.0) + 1
    spot_repeats = max(1, int((spot_end - spot_start - 0.8) / 0.5))

    if is_shorts:
        # High-Impact 100% Full-Bleed 9:16 Shorts 2.0 Composition
        html_content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Letter {letter} Phonics - ABC Zoo TV</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px; height: 1920px; overflow: hidden; background: #000000;
        font-family: Inter, ui-sans-serif, system-ui, sans-serif;
      }}
      #root {{
        position: relative; width: 100%; height: 100%; overflow: hidden;
      }}
      /* Edge-to-Edge Full-Bleed Viewport */
      #scene-stage {{
        position: absolute; inset: 0; width: 100%; height: 100%; overflow: hidden;
      }}
      .stage-scene {{
        position: absolute; inset: 0; width: 100%; height: 100%;
        object-fit: cover; object-position: center 32%;
        opacity: 0; transform-origin: center 35%;
      }}
      /* Floating Mascot Badge in Top Safe Zone */
      #badge-card {{
        position: absolute; top: 100px; left: 55px; z-index: 60;
      }}
      .badge-pill {{
        background: linear-gradient(135deg, #ffd700, #ff9100);
        border: 4.5px solid #ffffff;
        border-radius: 9999px;
        padding: 12px 36px;
        color: #0d1b2a;
        font-size: 38px;
        font-weight: 900;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6), 0 0 25px rgba(255, 215, 0, 0.45);
      }}
      /* Interactive Game Spotlight */
      #spotlight-layer {{
        position: absolute; inset: 0;
        display: flex; align-items: center; justify-content: center; pointer-events: none; z-index: 80;
        opacity: 0;
      }}
      .spotlight-inner {{
        width: 340px; height: auto; filter: drop-shadow(0 0 40px rgba(255, 215, 0, 0.95));
      }}
      /* Kinetic Subtitle Stream in Optical Safe Zone (Above YouTube UI) */
      #sub-container {{
        position: absolute; bottom: 400px; left: 0; width: 100%; height: 220px;
        display: flex; align-items: center; justify-content: center; z-index: 70;
        pointer-events: none;
      }}
      .sub-pill {{
        position: absolute; width: 920px; display: flex; align-items: center; justify-content: center;
        opacity: 0;
      }}
      .sub-inner {{
        background: rgba(13, 27, 42, 0.90);
        backdrop-filter: blur(16px);
        border: 4.5px solid #ffd700;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.75), 0 0 28px rgba(255, 215, 0, 0.45);
        border-radius: 9999px; padding: 20px 48px; text-align: center;
        font-size: 52px; font-weight: 900; color: #ffffff;
        line-height: 1.25;
        letter-spacing: -0.01em;
      }}
      .highlight {{
        color: #00ffcc; text-shadow: 0 0 18px rgba(0, 255, 204, 0.9); font-weight: 900;
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{total_duration}"
      data-width="1080"
      data-height="1920"
    >
      <!-- Edge-to-Edge 100% Full-Bleed 9:16 Visual Stage -->
      <div id="scene-stage">
        <img id="scene-1" class="stage-scene" src="scene_01.jpg" alt="Scene 1" />
        <img id="scene-2" class="stage-scene" src="scene_02.jpg" alt="Scene 2" />
        <img id="scene-3" class="stage-scene" src="scene_03.jpg" alt="Scene 3" />
      </div>

      <!-- Floating Mascot Badge in Top Safe Zone -->
      <div id="badge-card">
        <div class="badge-pill">{badge_text}</div>
      </div>

      <!-- Interactive Game Spotlight -->
      <div id="spotlight-layer">
        <img id="spotlight-img" class="spotlight-inner" src="spotlight.png" alt="Spotlight" />
      </div>

      <!-- Kinetic Subtitle Stream in Safe Zone -->
      <div id="sub-container">
{chr(10).join(sub_elements_html)}
      </div>

      <!-- Synchronized Soundtrack -->
      <audio id="soundtrack" src="soundtrack.wav" data-start="0" data-duration="{total_duration}" data-track-index="20"></audio>
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});

      // --- Scene 1 Motion: Dramatic Push-In on 3D Mascot ---
      tl.set("#scene-1", {{ opacity: 1, scale: 1.04 }}, 0);
      tl.fromTo("#scene-1", 
        {{ scale: 1.04, transformOrigin: "center 35%" }},
        {{ scale: 1.20, duration: {s1_dur}, ease: "power1.inOut" }}, 
        0
      );

      // --- Scene 2 Transition & Motion: Dynamic Parallax Squeeze ---
      tl.to("#scene-1", {{ opacity: 0, duration: 0.4, ease: "power2.inOut" }}, {s1_dur - 0.2});
      tl.fromTo("#scene-2", 
        {{ opacity: 0, scale: 1.22, x: -15, transformOrigin: "center 35%" }}, 
        {{ opacity: 1, scale: 1.10, x: 0, duration: 0.4, ease: "power2.inOut", immediateRender: false }}, 
        {s1_dur - 0.2}
      );
      tl.to("#scene-2",
        {{ scale: 1.20, x: 15, duration: {s2_dur}, ease: "sine.inOut" }},
        {s1_dur}
      );

      // --- Scene 3 Transition & Celebration Climax ---
      tl.to("#scene-2", {{ opacity: 0, duration: 0.4, ease: "power2.inOut" }}, {s1_dur + s2_dur - 0.2});
      tl.fromTo("#scene-3", 
        {{ opacity: 0, scale: 1.05, transformOrigin: "center 35%" }}, 
        {{ opacity: 1, scale: 1.24, duration: {s3_dur}, ease: "power1.out", immediateRender: false }}, 
        {s1_dur + s2_dur - 0.2}
      );

      // --- Floating Badge Gentle Sine Float ---
      tl.fromTo("#badge-card",
        {{ y: -6, rotation: -2 }},
        {{ y: 6, rotation: 2, duration: 1.8, repeat: {badge_repeats}, yoyo: true, ease: "sine.inOut" }},
        0
      );

      // --- Interactive Spotlight Game Animation ---
      tl.set("#spotlight-layer", {{ opacity: 0 }}, 0);
      tl.set("#spotlight-img", {{ scale: 0.4, opacity: 0, rotation: -20 }}, 0);
      tl.to("#spotlight-layer", {{ opacity: 1, duration: 0.2 }}, {spot_start});
      tl.to("#spotlight-img",
        {{ scale: 1.0, opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(2)" }},
        {spot_start}
      );
      tl.to("#spotlight-img",
        {{ scale: 1.15, duration: 0.5, repeat: {spot_repeats}, yoyo: true, ease: "sine.inOut" }},
        {spot_start + 0.5}
      );
      tl.to("#spotlight-layer",
        {{ opacity: 0, duration: 0.3, ease: "power2.in" }},
        {spot_end - 0.3}
      );

      // --- Kinetic Subtitles Stream ---
{chr(10).join(sub_animations_js)}

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
    else:
        # Smooth 16:9 Landscape Composition
        html_content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Letter {letter} Phonics - ABC Zoo TV</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1920px; height: 1080px; overflow: hidden; background: #000000;
        font-family: Inter, ui-sans-serif, system-ui, sans-serif;
      }}
      #root {{
        position: relative; width: 100%; height: 100%; overflow: hidden;
      }}
      #scene-stage {{
        position: absolute; inset: 0; width: 100%; height: 100%; overflow: hidden;
      }}
      .scene-img {{
        position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0;
        transform-origin: center center;
      }}
      #badge-card {{
        position: absolute; top: 60px; left: 70px; z-index: 60;
      }}
      .badge-img {{
        width: 220px; height: auto; filter: drop-shadow(0 12px 28px rgba(0, 0, 0, 0.6));
      }}
      .badge-pill {{
        background: linear-gradient(135deg, #ffd700, #ff9100);
        border: 4px solid #ffffff;
        border-radius: 9999px;
        padding: 12px 38px;
        color: #0d1b2a;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6), 0 0 25px rgba(255, 215, 0, 0.45);
      }}
      #sub-container {{
        position: absolute; bottom: 85px; left: 0; width: 100%; height: 180px;
        display: flex; align-items: center; justify-content: center; z-index: 70;
      }}
      .sub-pill {{
        position: absolute; width: 1400px; display: flex; align-items: center; justify-content: center;
        opacity: 0;
      }}
      .sub-inner {{
        background: rgba(13, 27, 42, 0.85);
        border: 4px solid #ffd700;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.7), 0 0 24px rgba(255, 215, 0, 0.4);
        border-radius: 40px; padding: 20px 50px; text-align: center;
        font-size: 56px; font-weight: 800; color: #ffffff;
        line-height: 1.3;
      }}
      .highlight {{
        color: #00ffcc; text-shadow: 0 0 16px rgba(0, 255, 204, 0.8); font-weight: 900;
      }}
      #spotlight-layer {{
        position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
        pointer-events: none; z-index: 80; opacity: 0;
      }}
      .spotlight-inner {{
        width: 320px; height: auto; filter: drop-shadow(0 0 35px rgba(255, 215, 0, 0.95));
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{total_duration}"
      data-width="1920"
      data-height="1080"
    >
      <!-- Main Scene Camera Stage -->
      <div id="scene-stage">
        <img id="scene-1" class="scene-img" src="scene_01.jpg" alt="Scene 1" />
        <img id="scene-2" class="scene-img" src="scene_02.jpg" alt="Scene 2" />
        <img id="scene-3" class="scene-img" src="scene_03.jpg" alt="Scene 3" />
      </div>

      <!-- Floating Mascot Badge -->
      <div id="badge-card">
        {f'<img id="badge-img" class="badge-img" src="badge.png" alt="Badge" />' if (hf_dir / "badge.png").exists() else f'<div class="badge-pill">{badge_text}</div>'}
      </div>

      <!-- Interactive Game Spotlight -->
      <div id="spotlight-layer">
        <img id="spotlight-img" class="spotlight-inner" src="spotlight.png" alt="Spotlight" />
      </div>

      <!-- Kinetic Subtitle Stream -->
      <div id="sub-container">
{chr(10).join(sub_elements_html)}
      </div>

      <!-- Synchronized Soundtrack -->
      <audio id="soundtrack" src="soundtrack.wav" data-start="0" data-duration="{total_duration}" data-track-index="20"></audio>
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});

      // --- Scene 1 Motion ---
      tl.set("#scene-1", {{ opacity: 1, scale: 1.0 }}, 0);
      tl.set("#scene-2", {{ opacity: 0 }}, 0);
      tl.set("#scene-3", {{ opacity: 0 }}, 0);
      tl.fromTo("#scene-1", 
        {{ scale: 1.0, transformOrigin: "center center" }},
        {{ scale: 1.12, duration: {s1_dur}, ease: "power1.inOut" }}, 
        0
      );

      // --- Scene 2 Transition & Motion ---
      tl.to("#scene-1", {{ opacity: 0, duration: 0.4, ease: "power2.inOut" }}, {s1_dur - 0.2});
      tl.fromTo("#scene-2", 
        {{ opacity: 0 }}, 
        {{ opacity: 1, duration: 0.4, ease: "power2.inOut", immediateRender: false }}, 
        {s1_dur - 0.2}
      );
      tl.fromTo("#scene-2",
        {{ scale: 1.12, x: -15 }},
        {{ scale: 1.0, x: 15, duration: {s2_dur}, ease: "power1.inOut", immediateRender: false }},
        {s1_dur}
      );

      // --- Scene 3 Transition & Motion ---
      tl.to("#scene-2", {{ opacity: 0, duration: 0.4, ease: "power2.inOut" }}, {s1_dur + s2_dur - 0.2});
      tl.fromTo("#scene-3", 
        {{ opacity: 0 }}, 
        {{ opacity: 1, duration: 0.4, ease: "power2.inOut", immediateRender: false }}, 
        {s1_dur + s2_dur - 0.2}
      );
      tl.fromTo("#scene-3",
        {{ scale: 1.0, y: 0 }},
        {{ scale: 1.15, y: -12, duration: {s3_dur}, ease: "power1.out", immediateRender: false }},
        {s1_dur + s2_dur}
      );

      // --- Floating Badge Sine Float ---
      tl.fromTo("#badge-card",
        {{ y: -8, rotation: -2.5 }},
        {{ y: 8, rotation: 2.5, duration: 2.0, repeat: {badge_repeats}, yoyo: true, ease: "sine.inOut" }},
        0
      );

      // --- Interactive Spotlight Game Animation ---
      tl.set("#spotlight-layer", {{ opacity: 0 }}, 0);
      tl.set("#spotlight-img", {{ scale: 0.4, opacity: 0, rotation: -20 }}, 0);
      tl.to("#spotlight-layer", {{ opacity: 1, duration: 0.2 }}, {spot_start});
      tl.to("#spotlight-img",
        {{ scale: 1.0, opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(2)" }},
        {spot_start}
      );
      tl.to("#spotlight-img",
        {{ scale: 1.18, duration: 0.5, repeat: {spot_repeats}, yoyo: true, ease: "sine.inOut" }},
        {spot_start + 0.5}
      );
      tl.to("#spotlight-layer",
        {{ opacity: 0, duration: 0.3, ease: "power2.in" }},
        {spot_end - 0.3}
      );

      // --- Kinetic Subtitles Stream ---
{chr(10).join(sub_animations_js)}

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

    with open(hf_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"✅ Generated HyperFrames composition for {output_format}: {hf_dir / 'index.html'}")
    return hf_dir

def render_episode_with_hyperframes(episode_dir, output_format="shorts", quality="looks", fps=60):
    hf_bin = check_hyperframes()
    episode_dir = Path(episode_dir)
    hf_dir = generate_hyperframes_composition(episode_dir, output_format=output_format)
    
    out_video = episode_dir / f"final_animated_{output_format}.mp4"
    print(f"🎬 Checking composition integrity with HyperFrames check...")
    
    env = os.environ.copy()
    env["HYPERFRAMES_SKIP_SKILLS"] = "1"
    
    check_cmd = [hf_bin, "check", str(hf_dir)]
    check_res = subprocess.run(check_cmd, cwd=str(BASE_DIR), env=env, capture_output=True, text=True)
    if check_res.returncode != 0:
        print(f"⚠️ HyperFrames check warnings/output:\n{check_res.stdout}\n{check_res.stderr}")
    else:
        print(f"✨ HyperFrames composition passed all lint & runtime checks!")
        
    print(f"🚀 Rendering 60fps buttery-smooth video to: {out_video.name}...")
    render_cmd = [
        hf_bin, "render", str(hf_dir),
        "--fps", str(fps),
        "--quality", quality,
        "-o", str(out_video)
    ]
    render_res = subprocess.run(render_cmd, cwd=str(BASE_DIR), env=env, capture_output=True, text=True)
    if render_res.returncode != 0:
        print(f"❌ Render failed:\n{render_res.stdout}\n{render_res.stderr}")
        raise RuntimeError("HyperFrames render failed.")
        
    print(f"🎉 Successfully rendered {output_format.upper()} video via HyperFrames! Size: {out_video.stat().st_size / (1024*1024):.2f} MB")
    return out_video

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render smooth episode video with HyperFrames")
    parser.add_argument("episode_dir", help="Path to episode directory")
    parser.add_argument("--format", choices=["landscape", "shorts", "both"], default="shorts", help="Output format")
    parser.add_argument("--quality", choices=["draft", "looks", "delivery"], default="looks", help="Render quality")
    parser.add_argument("--fps", type=int, default=60, help="Framerate (default: 60)")
    
    args = parser.parse_args()
    formats = ["landscape", "shorts"] if args.format == "both" else [args.format]
    
    for fmt in formats:
        render_episode_with_hyperframes(args.episode_dir, output_format=fmt, quality=args.quality, fps=args.fps)
