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

def generate_hyperframes_composition(episode_dir, output_format="shorts", theme_index=0):
    episode_dir = Path(episode_dir)
    is_shorts = (output_format == "shorts")
    w = 1080 if is_shorts else 1920
    h = 1920 if is_shorts else 1080
    
    # 1. Parse Letter and Character metadata
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
    
    # 3. Load Voice Manifest or calculate from segments
    voice_manifest = episode_dir / "neural_vocals" / "voice_manifest.json"
    if voice_manifest.exists():
        with open(voice_manifest, "r", encoding="utf-8") as f:
            voice_segs = json.load(f)
    else:
        # Fallback to standard timeline
        voice_segs = [
            {"index": 0, "text": f"Hi friends! I am {char_name} the {animal_name}!", "start": 0.2, "end": 2.8},
            {"index": 1, "text": f"Look what I found... It is the Letter {letter}!", "start": 3.2, "end": 6.2},
            {"index": 2, "text": f"Can you say {letter} with me? {letter}! {letter}! {obj_name}!", "start": 6.8, "end": 10.2},
            {"index": 3, "text": f"{letter} is for {char_name}, playing every day!", "start": 10.8, "end": 13.8},
            {"index": 4, "text": f"{letter} is for {obj_name}, hip hip hooray!", "start": 14.2, "end": 17.0},
            {"index": 5, "text": f"Can you find the {obj_name.lower()}? Point to it!", "start": 17.5, "end": 20.2},
            {"index": 6, "text": f"You found it! Good job! High five!", "start": 20.8, "end": 23.2},
            {"index": 7, "text": f"See you next time with {next_char}! Bye-bye!", "start": 23.8, "end": 26.5}
        ]
        
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
        st = seg["start"]
        et = voice_segs[i+1]["start"] - 0.15 if i+1 < len(voice_segs) else total_duration - 0.5
        text = seg["text"]
        
        # Color highlight
        display_text = text
        for kw in [f"Letter {letter}", letter, char_name, obj_name]:
            if kw in display_text:
                display_text = display_text.replace(kw, f'<span class="highlight">{kw}</span>')
                
        sub_elements_html.append(
            f'        <div id="sub-{i}" class="sub-pill">\n'
            f'          <div class="sub-inner">{display_text}</div>\n'
            f'        </div>'
        )
        
        sub_animations_js.append(
            f'      // Subtitle {i}\n'
            f'      tl.fromTo("#sub-{i}", {{ opacity: 0, y: 15, scale: 0.85 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {st});\n'
            f'      tl.to("#sub-{i}", {{ opacity: 0, y: -10, duration: 0.2, ease: "power2.in" }}, {et - 0.2});'
        )

    spot_start = round(voice_segs[5]["start"], 2)
    spot_end = round(voice_segs[6]["start"] + 0.3, 2)
    badge_repeats = int(total_duration / 2.0) + 1
    spot_repeats = max(1, int((spot_end - spot_start - 0.8) / 0.5))

    if is_shorts:
        # Triple-Tier Smooth 9:16 Shorts Composition
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
        width: 1080px; height: 1920px; overflow: hidden; background: #0b0f19;
        font-family: Inter, ui-sans-serif, system-ui, sans-serif;
      }}
      #root {{
        position: relative; width: 100%; height: 100%; overflow: hidden;
      }}
      #ambient-bg {{
        position: absolute; inset: -40px; overflow: hidden; filter: blur(35px) brightness(0.85) saturate(1.3);
      }}
      .ambient-img {{
        position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0;
      }}
      #stage-card {{
        position: absolute; top: 480px; left: 20px; width: 1040px; height: 585px;
        border-radius: 32px; overflow: hidden;
        border: 6px solid rgba(255, 255, 255, 0.95);
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.6), 0 0 30px rgba(255, 215, 0, 0.3);
        background: #000;
      }}
      .stage-scene {{
        position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0;
        transform-origin: center center;
      }}
      #header-banner {{
        position: absolute; top: 160px; left: 0; width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; z-index: 50;
      }}
      .header-title {{
        font-size: 64px; font-weight: 900; color: #ffd700;
        text-shadow: 0 4px 16px rgba(0, 0, 0, 0.8), 0 0 24px rgba(255, 215, 0, 0.5);
        letter-spacing: 0.05em; text-transform: uppercase;
      }}
      .header-sub {{
        font-size: 42px; font-weight: 700; color: #ffffff;
        text-shadow: 0 3px 12px rgba(0, 0, 0, 0.8);
        margin-top: 8px;
      }}
      #badge-card {{
        position: absolute; top: 60px; left: 60px; z-index: 60;
      }}
      .badge-img {{
        width: 180px; height: auto; filter: drop-shadow(0 10px 25px rgba(0, 0, 0, 0.5));
      }}
      #sub-container {{
        position: absolute; top: 1250px; left: 0; width: 100%; height: 260px;
        display: flex; align-items: center; justify-content: center; z-index: 70;
      }}
      .sub-pill {{
        position: absolute; width: 920px; display: flex; align-items: center; justify-content: center;
        opacity: 0;
      }}
      .sub-inner {{
        background: rgba(13, 27, 42, 0.85);
        border: 4px solid #ffd700;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6), 0 0 20px rgba(255, 215, 0, 0.35);
        border-radius: 40px; padding: 24px 44px; text-align: center;
        font-size: 48px; font-weight: 800; color: #ffffff;
        line-height: 1.3;
      }}
      .highlight {{
        color: #00ffcc; text-shadow: 0 0 15px rgba(0, 255, 204, 0.8); font-weight: 900;
      }}
      #spotlight-layer {{
        position: absolute; top: 480px; left: 20px; width: 1040px; height: 585px;
        display: flex; align-items: center; justify-content: center; pointer-events: none; z-index: 80;
        opacity: 0;
      }}
      .spotlight-inner {{
        width: 280px; height: auto; filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.9));
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
      <!-- Background Ambient Glow -->
      <div id="ambient-bg">
        <img id="amb-1" class="ambient-img" src="amb_01.jpg" alt="" />
        <img id="amb-2" class="ambient-img" src="amb_02.jpg" alt="" />
        <img id="amb-3" class="ambient-img" src="amb_03.jpg" alt="" />
      </div>

      <!-- Top Header Title Banner -->
      <div id="header-banner">
        <h1 class="header-title">LETTER {letter} PHONICS</h1>
        <h2 class="header-sub">{char_name} the {animal_name} &amp; {obj_name}</h2>
      </div>

      <!-- Floating Mascot Badge -->
      <div id="badge-card">
        <img id="badge-img" class="badge-img" src="badge.png" alt="Badge" />
      </div>

      <!-- Center 16:9 Main Cinema Stage -->
      <div id="stage-card">
        <img id="scene-1" class="stage-scene" src="scene_01.jpg" alt="Scene 1" />
        <img id="scene-2" class="stage-scene" src="scene_02.jpg" alt="Scene 2" />
        <img id="scene-3" class="stage-scene" src="scene_03.jpg" alt="Scene 3" />
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
      tl.set("#amb-1, #scene-1", {{ opacity: 1 }}, 0);
      tl.fromTo("#scene-1", 
        {{ scale: 1.0, transformOrigin: "center center" }},
        {{ scale: 1.10, duration: {s1_dur}, ease: "power1.inOut" }}, 
        0
      );

      // --- Scene 2 Transition & Motion ---
      tl.to("#amb-1, #scene-1", {{ opacity: 0, duration: 0.4, ease: "power2.inOut" }}, {s1_dur - 0.2});
      tl.fromTo("#amb-2, #scene-2", 
        {{ opacity: 0 }}, 
        {{ opacity: 1, duration: 0.4, ease: "power2.inOut" }}, 
        {s1_dur - 0.2}
      );
      tl.fromTo("#scene-2",
        {{ scale: 1.10, x: -10 }},
        {{ scale: 1.0, x: 10, duration: {s2_dur}, ease: "power1.inOut" }},
        {s1_dur}
      );

      // --- Scene 3 Transition & Motion ---
      tl.to("#amb-2, #scene-2", {{ opacity: 0, duration: 0.4, ease: "power2.inOut" }}, {s1_dur + s2_dur - 0.2});
      tl.fromTo("#amb-3, #scene-3", 
        {{ opacity: 0 }}, 
        {{ opacity: 1, duration: 0.4, ease: "power2.inOut" }}, 
        {s1_dur + s2_dur - 0.2}
      );
      tl.fromTo("#scene-3",
        {{ scale: 1.0, y: 0 }},
        {{ scale: 1.12, y: -8, duration: {s3_dur}, ease: "power1.out" }},
        {s1_dur + s2_dur}
      );

      // --- Floating Badge Gentle Sine Float ---
      tl.fromTo("#badge-img",
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
        <img id="badge-img" class="badge-img" src="badge.png" alt="Badge" />
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
      tl.set("#scene-1", {{ opacity: 1 }}, 0);
      tl.fromTo("#scene-1", 
        {{ scale: 1.0, transformOrigin: "center center" }},
        {{ scale: 1.12, duration: {s1_dur}, ease: "power1.inOut" }}, 
        0
      );

      // --- Scene 2 Transition & Motion ---
      tl.to("#scene-1", {{ opacity: 0, duration: 0.4, ease: "power2.inOut" }}, {s1_dur - 0.2});
      tl.fromTo("#scene-2", 
        {{ opacity: 0 }}, 
        {{ opacity: 1, duration: 0.4, ease: "power2.inOut" }}, 
        {s1_dur - 0.2}
      );
      tl.fromTo("#scene-2",
        {{ scale: 1.12, x: -15 }},
        {{ scale: 1.0, x: 15, duration: {s2_dur}, ease: "power1.inOut" }},
        {s1_dur}
      );

      // --- Scene 3 Transition & Motion ---
      tl.to("#scene-2", {{ opacity: 0, duration: 0.4, ease: "power2.inOut" }}, {s1_dur + s2_dur - 0.2});
      tl.fromTo("#scene-3", 
        {{ opacity: 0 }}, 
        {{ opacity: 1, duration: 0.4, ease: "power2.inOut" }}, 
        {s1_dur + s2_dur - 0.2}
      );
      tl.fromTo("#scene-3",
        {{ scale: 1.0, y: 0 }},
        {{ scale: 1.15, y: -12, duration: {s3_dur}, ease: "power1.out" }},
        {s1_dur + s2_dur}
      );

      // --- Floating Badge Sine Float ---
      tl.fromTo("#badge-img",
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
        "--non-interactive",
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
