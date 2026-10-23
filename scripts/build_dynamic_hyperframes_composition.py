#!/usr/bin/env python3
"""
Enhanced Dynamic HyperFrames Composition Generator for Routine & Action Episodes.
Injects:
1. Animated flowing water stream & splashing droplets
2. 24 floating iridescent soap bubbles with physics wobble & pop
3. Vigorous 5Hz hand-scrubbing foam motion
4. Golden sparkle stars & confetti clean celebration
"""

import os
import sys
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def build_dynamic_composition(episode_dir, output_format="landscape"):
    ep_dir = Path(episode_dir).resolve()
    is_shorts = (output_format == "shorts")
    hf_dir = ep_dir / f"hyperframes_{output_format}"
    hf_dir.mkdir(parents=True, exist_ok=True)

    with open(ep_dir / "voice_timeline.json", "r", encoding="utf-8") as f:
        voice_segs = json.load(f)

    total_duration = round(voice_segs[-1]["end"] + 2.2, 2)
    s1_dur = round(voice_segs[3]["start"] + 0.3, 2)
    s2_dur = round(voice_segs[6]["start"] - s1_dur + 0.2, 2)
    s3_dur = round(total_duration - s1_dur - s2_dur, 2)

    width = 1080 if is_shorts else 1920
    height = 1920 if is_shorts else 1080

    # Scene images
    if is_shorts and (ep_dir / "shorts_scene_01.jpg").exists():
        s1_file = "shorts_scene_01.jpg"
        s2_file = "shorts_scene_02.jpg"
        s3_file = "shorts_scene_03.jpg"
    else:
        s1_file = "scene_01_hook.jpg"
        s2_file = "scene_02_dancing.jpg"
        s3_file = "scene_03_celebration.jpg"

    # Copy files
    for src_name, dst_name in [
        (s1_file, "scene_01.jpg"),
        (s2_file, "scene_02.jpg"),
        (s3_file, "scene_03.jpg"),
        ("soundtrack_with_vocals.wav", "soundtrack.wav"),
        ("spotlight_pointer.png", "spotlight.png")
    ]:
        src = ep_dir / src_name
        dst = hf_dir / dst_name
        if src.exists():
            import shutil
            shutil.copyfile(str(src), str(dst))

    with open(hf_dir / "hyperframes.json", "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "composition": "main",
            "duration": total_duration,
            "fps": 60,
            "width": width,
            "height": height
        }, f, indent=2)

    # Subtitles
    sub_elements_html = []
    sub_animations_js = []
    for i, seg in enumerate(voice_segs):
        st = round(seg["start"], 2)
        speech_end = round(seg["end"], 2)
        next_st = round(voice_segs[i+1]["start"], 2) if i+1 < len(voice_segs) else total_duration - 0.4
        et = round(min(speech_end + 0.35, next_st - 0.10), 2)
        text = seg["text"]

        # Highlight keywords
        display_text = text
        for kw in ["Henry", "Barnaby", "wash our hands", "bubbly soap", "Splish, splash", "Super clean!"]:
            if kw in display_text:
                display_text = re.sub(r'\b' + re.escape(kw) + r'\b', f'<span class="highlight">{kw}</span>', display_text)

        sub_elements_html.append(
            f'        <div id="sub-{i}" class="sub-pill">\n'
            f'          <div class="sub-inner">{display_text}</div>\n'
            f'        </div>'
        )
        fade_out = round(max(st + 0.3, et - 0.2), 2)
        sub_animations_js.append(
            f'      // Subtitle {i}\n'
            f'      tl.fromTo("#sub-{i}", {{ opacity: 0, y: 15, scale: 0.88 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {st});\n'
            f'      tl.to("#sub-{i}", {{ opacity: 0, y: -10, duration: 0.2, ease: "power2.in" }}, {fade_out});'
        )

    # Faucet & Hands Coordinates
    if is_shorts:
        faucet_x, faucet_y = 310, 1020
        stream_h = 320
        stream_w = 28
        hands_x, hands_y = 530, 1220
        foam_w, foam_h = 240, 180
    else:
        faucet_x, faucet_y = 390, 520
        stream_h = 200
        stream_w = 22
        hands_x, hands_y = 920, 620
        foam_w, foam_h = 220, 160

    # Generate 14 soap bubbles with clean separate wrapper/inner animation
    import random
    random.seed(42) # Deterministic
    bubbles_html = []
    bubbles_js = []
    for b_i in range(14):
        b_size = random.randint(35, 95) if not is_shorts else random.randint(45, 125)
        b_start_x = random.randint(40, width - 40 - b_size)
        b_start_y = height + random.randint(20, 350)
        b_delay = round(random.uniform(0.1, max(0.5, total_duration - 4.5)), 2)
        b_float_dur = round(random.uniform(5.5, 9.5), 2)
        wobble_x = random.randint(25, 45)

        bubbles_html.append(
            f'        <div id="bubble-wrap-{b_i}" class="soap-bubble-wrap" style="left:{b_start_x}px; top:{b_start_y}px;">'
            f'<div id="bubble-{b_i}" class="soap-bubble" style="width:{b_size}px; height:{b_size}px;"></div></div>'
        )
        bubbles_js.append(
            f'      tl.fromTo("#bubble-wrap-{b_i}", {{ y: 0, opacity: 0.95 }}, {{ y: -({height + 500}), duration: {b_float_dur}, ease: "none" }}, {b_delay});\n'
            f'      tl.fromTo("#bubble-{b_i}", {{ x: -{wobble_x} }}, {{ x: {wobble_x}, duration: 1.2, repeat: 7, yoyo: true, ease: "sine.inOut" }}, {b_delay});'
        )

    # Splash droplets
    splash_html = []
    splash_js = []
    for s_i in range(6):
        angle = random.uniform(-1.2, 1.2)
        dist = random.uniform(30, 85)
        dx = round(dist * angle, 1)
        dy = round(-random.uniform(40, 100), 1)
        splash_html.append(f'        <div id="drop-{s_i}" class="splash-drop" style="left:{faucet_x + stream_w // 2}px; top:{faucet_y + stream_h}px;"></div>')
        # Repeating splash loops during Scene 1 and 2
        splash_js.append(
            f'      tl.fromTo("#drop-{s_i}", {{ x: 0, y: 0, opacity: 1, scale: 1 }}, {{ x: {dx}, y: {dy}, opacity: 0, scale: 0.3, duration: 0.45, repeat: 48, ease: "power1.out" }}, 0.2);'
        )

    # Stars for Scene 3 clean hands celebration (SVG graphics, no text overlap)
    stars_html = []
    stars_js = []
    scene3_start = s1_dur + s2_dur
    for st_i in range(12):
        offset_x = random.randint(-180, 180)
        offset_y = random.randint(-120, 120)
        st_size = random.randint(32, 60)
        star_x = hands_x + offset_x
        star_y = hands_y + offset_y
        delay_offset = round(random.uniform(0.1, 1.8), 2)
        stars_html.append(
            f'        <svg id="star-{st_i}" class="sparkle-star" width="{st_size}" height="{st_size}" viewBox="0 0 24 24" '
            f'data-layout-allow-overlap="true" data-layout-allow-occlusion="true" '
            f'style="left:{star_x}px; top:{star_y}px;">'
            f'<polygon points="12,2 15,9 22,9 17,14 19,21 12,17 5,21 7,14 2,9 9,9" fill="#ffd600" stroke="#ffffff" stroke-width="1.5"/>'
            f'</svg>'
        )
        stars_js.append(
            f'      tl.fromTo("#star-{st_i}", {{ scale: 0, rotation: 0, opacity: 0 }}, {{ scale: 1.3, rotation: 180, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, {scene3_start + delay_offset});\n'
            f'      tl.to("#star-{st_i}", {{ scale: 0.8, rotation: 360, duration: 0.5, repeat: 8, yoyo: true, ease: "sine.inOut" }}, {scene3_start + delay_offset + 0.45});'
        )

    badge_repeats = int(total_duration / 2.0) + 1
    spot_start = round(voice_segs[5]["start"], 2)
    spot_end = round(voice_segs[6]["start"] + 0.25, 2)
    spot_repeats = max(1, int((spot_end - spot_start - 0.8) / 0.5))

    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={width}, height={height}" />
    <title>Wash Your Hands Song - ABC Zoo TV</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{
        font-family: 'Arial Rounded MT Bold';
        src: local('Arial Rounded MT Bold'), local('ArialRoundedMTBold');
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: {width}px; height: {height}px; overflow: hidden; background: #000000;
        font-family: 'Arial Rounded MT Bold', Inter, -apple-system, sans-serif;
      }}
      #root {{
        position: relative; width: 100%; height: 100%; overflow: hidden;
      }}
      #scene-stage {{
        position: absolute; inset: 0; width: 100%; height: 100%; overflow: hidden;
      }}
      .stage-scene {{
        position: absolute; inset: 0; width: 100%; height: 100%;
        object-fit: cover; object-position: center {"32%" if is_shorts else "center"};
        opacity: 0; transform-origin: center {"35%" if is_shorts else "center"};
      }}
      /* Faucet Water Stream */
      #water-stream {{
        position: absolute;
        left: {faucet_x}px; top: {faucet_y}px;
        width: {stream_w}px; height: {stream_h}px;
        background: linear-gradient(180deg, #ffffff 0%, #40c4ff 40%, #00b0ff 100%);
        border-radius: 14px;
        box-shadow: 0 0 16px rgba(0,229,255,0.9);
        z-index: 50;
        transform-origin: top center;
      }}
      /* Splashing Droplets */
      .splash-drop {{
        position: absolute; width: 14px; height: 14px; border-radius: 50%;
        background: #40c4ff;
        border: 2px solid #ffffff;
        box-shadow: 0 0 10px rgba(0,229,255,0.95);
        z-index: 51; opacity: 0;
      }}
      /* Hand Scrubbing Soap Foam Layer */
      #scrub-foam {{
        position: absolute;
        left: {hands_x - foam_w // 2}px; top: {hands_y - foam_h // 2}px;
        width: {foam_w}px; height: {foam_h}px;
        background: radial-gradient(circle at 45% 45%, rgba(255,255,255,0.98) 0%, rgba(224,247,250,0.85) 45%, rgba(178,235,242,0.6) 75%, rgba(255,255,255,0) 100%);
        border-radius: 50%;
        box-shadow: 0 0 25px rgba(255,255,255,0.95);
        z-index: 52;
        transform-origin: center center;
      }}
      /* Floating Iridescent Soap Bubbles */
      .soap-bubble-wrap {{
        position: absolute;
        pointer-events: none;
        z-index: 55;
      }}
      .soap-bubble {{
        position: relative;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.45);
        border: 2.5px solid rgba(255, 255, 255, 0.9);
        box-shadow: inset -4px -4px 10px rgba(0, 190, 255, 0.45), 0 0 14px rgba(255, 255, 255, 0.85);
      }}
      .soap-bubble::after {{
        content: ''; position: absolute; top: 15%; left: 20%; width: 26%; height: 16%;
        border-radius: 50%; background: rgba(255,255,255,0.95); transform: rotate(-30deg);
      }}
      /* Clean Hands Sparkling Stars */
      .sparkle-star {{
        position: absolute; color: #ffd600;
        text-shadow: 0 0 18px rgba(255,214,0,0.95), 0 0 35px rgba(255,145,0,0.8);
        z-index: 58; pointer-events: none; opacity: 0;
      }}
      /* Badge */
      #badge-card {{
        position: absolute; top: {"100px" if is_shorts else "60px"}; left: {"55px" if is_shorts else "70px"}; z-index: 60;
      }}
      .badge-pill {{
        background: linear-gradient(135deg, #ffd700, #ff9100);
        border: 4.5px solid #ffffff;
        border-radius: 9999px;
        padding: 14px 42px;
        color: #0d1b2a;
        font-size: {"38px" if is_shorts else "34px"};
        font-weight: 900;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 14px 35px rgba(0,0,0,0.65), 0 0 28px rgba(255,215,0,0.5);
      }}
      /* Subtitles */
      #sub-container {{
        position: absolute; bottom: {"400px" if is_shorts else "85px"}; left: 0; width: 100%; height: {"220px" if is_shorts else "180px"};
        display: flex; align-items: center; justify-content: center; z-index: 70;
        pointer-events: none;
      }}
      .sub-pill {{
        position: absolute; width: {"920px" if is_shorts else "1400px"}; display: flex; align-items: center; justify-content: center;
        opacity: 0;
      }}
      .sub-inner {{
        background: rgba(13, 27, 42, 0.88);
        border: 4.5px solid #ffd700;
        box-shadow: 0 14px 40px rgba(0,0,0,0.75), 0 0 30px rgba(255,215,0,0.45);
        border-radius: 40px; padding: {"22px 36px" if is_shorts else "20px 50px"}; text-align: center;
        font-size: {"52px" if is_shorts else "56px"}; font-weight: 900; color: #ffffff;
        line-height: 1.3;
      }}
      .highlight {{
        color: #00ffcc; text-shadow: 0 0 18px rgba(0,255,204,0.9); font-weight: 900;
      }}
      #spotlight-layer {{
        position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
        pointer-events: none; z-index: 80; opacity: 0;
      }}
      .spotlight-inner {{
        width: {"340px" if is_shorts else "320px"}; height: auto; filter: drop-shadow(0 0 40px rgba(255,215,0,0.95));
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{total_duration}"
      data-width="{width}"
      data-height="{height}"
    >
      <!-- Main Scene Camera Stage -->
      <div id="scene-stage" data-layout-allow-overflow="true">
        <img id="scene-1" class="stage-scene" src="scene_01.jpg" alt="Scene 1" data-layout-allow-overflow="true" />
        <img id="scene-2" class="stage-scene" src="scene_02.jpg" alt="Scene 2" data-layout-allow-overflow="true" />
        <img id="scene-3" class="stage-scene" src="scene_03.jpg" alt="Scene 3" data-layout-allow-overflow="true" />
      </div>

      <!-- Flowing Water Stream & Droplets -->
      <div id="water-stream" data-layout-allow-overlap="true" data-layout-allow-occlusion="true"></div>
{chr(10).join(splash_html)}

      <!-- Active Hand Scrubbing Foam -->
      <div id="scrub-foam" data-layout-allow-overlap="true" data-layout-allow-occlusion="true"></div>

      <!-- Floating Soap Bubbles Layer -->
{chr(10).join(bubbles_html)}

      <!-- Clean Hands Sparkle Stars -->
{chr(10).join(stars_html)}

      <!-- Floating Mascot Badge -->
      <div id="badge-card" data-layout-allow-overlap="true">
        <div class="badge-pill">WASH HANDS 🧼</div>
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

      // --- Scene 3 Transition & Celebration ---
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

      // --- Flowing Water Animation ---
      tl.fromTo("#water-stream",
        {{ scaleX: 0.88, opacity: 0.9 }},
        {{ scaleX: 1.12, opacity: 1, duration: 0.22, repeat: 120, yoyo: true, ease: "sine.inOut" }},
        0
      );
      tl.to("#water-stream", {{ opacity: 0, duration: 0.4 }}, {scene3_start});

      // --- Active Hand Scrubbing Motion ---
      tl.fromTo("#scrub-foam",
        {{ scale: 0.94, rotation: -12, x: -8 }},
        {{ scale: 1.12, rotation: 12, x: 8, duration: 0.20, repeat: 130, yoyo: true, ease: "sine.inOut" }},
        0
      );
      tl.to("#scrub-foam", {{ opacity: 0, duration: 0.4 }}, {scene3_start});

      // --- Water Splashes ---
{chr(10).join(splash_js)}

      // --- Floating Soap Bubbles Drift ---
{chr(10).join(bubbles_js)}

      // --- Clean Hands Celebration Sparkles ---
{chr(10).join(stars_js)}

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
        f.write(html)

    print(f"✅ Generated Dynamic Action HyperFrames composition: {hf_dir / 'index.html'}")
    return hf_dir

if __name__ == "__main__":
    ep = sys.argv[1] if len(sys.argv) > 1 else "episodes/Ep_030_Wash_Hands"
    fmt = sys.argv[2] if len(sys.argv) > 2 else "landscape"
    build_dynamic_composition(ep, fmt)
