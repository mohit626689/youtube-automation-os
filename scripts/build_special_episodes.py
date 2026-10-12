#!/usr/bin/env python3
"""
ABC Zoo TV — Special Episodes Assembler & Scheduler (Days 27, 28, 29)
Produces and schedules:
- Day 27: Complete A to Z Phonics Alphabet Song (All 26 Mascots Ensemble)
- Day 28: Phase 2 Ep 027 — Brush Your Teeth Song: 2-Minute Sparkle Routine (Barnaby & Coco)
- Day 29: Phase 2 Ep 028 — Good Morning, Wake Up! The Happy Sunrise Song (Allie & Danny)
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Import audio and compositor tools
sys.path.append(str(BASE_DIR / "scripts"))
from generate_animated_episode import (
    synthesize_cartoon_sfx,
    build_complete_audio,
    generate_animated_ass_subtitles,
    generate_interactive_spotlight_png,
    SUBTITLE_THEMES
)
from render_hyperframes_episode import render_episode_with_hyperframes

SPECIAL_EPISODES = [
    {
        "id_base": 27,
        "folder": "episodes/Ep_027_AZ_Compilation",
        "badge": "ABC SONGS",
        "day": 27,
        "date_ist_morning": "2026-10-21 08:00 AM IST",
        "date_utc_morning": "2026-10-21T02:30:00Z",
        "date_ist_evening": "2026-10-21 05:00 PM IST",
        "date_utc_evening": "2026-10-21T11:30:00Z",
        "meta_filename": "metadata_az_compilation.json",
        "title_landscape": "Complete A to Z Phonics Alphabet Song 🎈 All 26 ABC Zoo Friends Sing & Dance! | ABC Zoo TV",
        "title_shorts": "Can You Sing the Whole ABC Song? 🎈 Alphabet Dance #Shorts",
        "images": {
            "hero": "/Users/shivpratap/.gemini/antigravity/brain/98558d5e-a99d-4007-8cee-f84164055600/az_compilation_hero_1791808406308.jpg",
            "s1": "/Users/shivpratap/.gemini/antigravity/brain/98558d5e-a99d-4007-8cee-f84164055600/az_compilation_hero_1791808406308.jpg",
            "s2": "/Users/shivpratap/.gemini/antigravity/brain/98558d5e-a99d-4007-8cee-f84164055600/az_compilation_hero_1791808406308.jpg",
            "s3": "/Users/shivpratap/.gemini/antigravity/brain/98558d5e-a99d-4007-8cee-f84164055600/az_compilation_hero_1791808406308.jpg",
        },
        "lines": [
            "Hi friends! We know all 26 letters of the alphabet!",
            "Let us sing and dance the whole ABC song together!",
            "A, B, C, D, E, F, G! H, I, J, K, L, M, N, O, P!",
            "Q, R, S, T, U, V! W, X, Y and Z!",
            "Now we know our A B Cs, next time won't you sing with me?",
            "Can you clap your hands to the beat? Clap, clap, clap!",
            "You did it! You know the whole alphabet! High five!",
            "Get ready for healthy routine adventures next time! Bye-bye!"
        ]
    },
    {
        "id_base": 28,
        "folder": "episodes/Ep_028_Brush_Teeth",
        "badge": "BRUSH TEETH",
        "day": 28,
        "date_ist_morning": "2026-10-22 08:00 AM IST",
        "date_utc_morning": "2026-10-22T02:30:00Z",
        "date_ist_evening": "2026-10-22 05:00 PM IST",
        "date_utc_evening": "2026-10-22T11:30:00Z",
        "meta_filename": "metadata_brush_teeth.json",
        "title_landscape": "Brush Your Teeth Song 🪥 Barnaby Bear & Coco Cat Sparkle Routine | ABC Zoo TV",
        "title_shorts": "Brush, Brush, Brush Your Teeth! 🪥 Sparkle Smile #Shorts",
        "images": {
            "hero": str(BASE_DIR / "episodes/Ep_002_Letter_B/thumbnail_hero.jpg"),
            "s1": str(BASE_DIR / "episodes/Ep_002_Letter_B/scene_01_hook.jpg"),
            "s2": str(BASE_DIR / "episodes/Ep_003_Letter_C/scene_01_hook.jpg"),
            "s3": str(BASE_DIR / "episodes/Ep_002_Letter_B/scene_03_celebration.jpg"),
        },
        "lines": [
            "Hi friends! Barnaby and Coco are ready to brush our teeth!",
            "Grab your toothbrush and let us make our smiles sparkle!",
            "Brush, brush, brush your teeth, round and round and clean!",
            "Up and down and all around, the brightest smile you've seen!",
            "Swish, spit, rinse it out, hip hip hooray!",
            "Can you show me your big shiny smile? Say cheese!",
            "Super sparkle! Clean teeth every morning and night!",
            "See you tomorrow for morning wake up! Bye-bye!"
        ]
    },
    {
        "id_base": 29,
        "folder": "episodes/Ep_029_Morning_Wakeup",
        "badge": "GOOD MORNING",
        "day": 29,
        "date_ist_morning": "2026-10-23 08:00 AM IST",
        "date_utc_morning": "2026-10-23T02:30:00Z",
        "date_ist_evening": "2026-10-23 05:00 PM IST",
        "date_utc_evening": "2026-10-23T11:30:00Z",
        "meta_filename": "metadata_morning_wakeup.json",
        "title_landscape": "Good Morning Wake Up Song ☀️ Allie & Danny Happy Sunrise Routine | ABC Zoo TV",
        "title_shorts": "Good Morning, Time to Wake Up! ☀️ Stretch & Smile #Shorts",
        "images": {
            "hero": str(BASE_DIR / "episodes/Ep_001_Letter_A/thumbnail_hero.jpg"),
            "s1": str(BASE_DIR / "episodes/Ep_001_Letter_A/scene_01_hook.jpg"),
            "s2": str(BASE_DIR / "episodes/Ep_004_Letter_D/scene_01_hook.jpg"),
            "s3": str(BASE_DIR / "episodes/Ep_001_Letter_A/scene_03_celebration.jpg"),
        },
        "lines": [
            "Good morning friends! The golden sun is up in the sky!",
            "Allie and Danny are stretching and ready for a happy new day!",
            "Wake up, wake up, stretch up high, touch the morning sun!",
            "Make your bed and brush your teeth, today will be so fun!",
            "Sunny day, smiling friends, hip hip hooray!",
            "Can you stretch your arms all the way up? Stretch, stretch, stretch!",
            "Great stretching! You are full of morning energy! High five!",
            "See you next time with Henry Hippo! Bye-bye!"
        ]
    }
]

def setup_episode(spec):
    ep_dir = BASE_DIR / spec["folder"]
    ep_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Images
    shutil.copy2(spec["images"]["hero"], ep_dir / "thumbnail_hero.jpg")
    shutil.copy2(spec["images"]["s1"], ep_dir / "scene_01_hook.jpg")
    shutil.copy2(spec["images"]["s2"], ep_dir / "scene_02_dancing.jpg")
    shutil.copy2(spec["images"]["s3"], ep_dir / "scene_03_celebration.jpg")

    # 2. Badge text
    (ep_dir / "badge_text.txt").write_text(spec["badge"], encoding="utf-8")

    # 3. Lines JSON
    lines_path = ep_dir / "lines.json"
    with open(lines_path, "w", encoding="utf-8") as f:
        json.dump(spec["lines"], f, indent=2)

    # 4. Neural vocals
    voice_script = BASE_DIR / "scripts" / "synthesize_custom_voice.js"
    print(f"🎙️ Generating voiceover for {ep_dir.name}...")
    subprocess.run(["node", str(voice_script), str(ep_dir), str(lines_path), "en-US-AnaNeural"], check=True)

    # 5. Metadata JSON for uploader
    meta = {
        "title": spec["title_landscape"],
        "title_shorts": spec["title_shorts"],
        "description": f"{spec['title_landscape']}\n\nSing, dance, and learn with ABC Zoo TV! Educational videos designed for toddlers and preschoolers (ages 1-5).",
        "tags": [
            "ABC Zoo TV", "Toddler Songs", "Nursery Rhymes", "Kids Animation", "Preschool Learning", "Educational Videos", "Kids Songs"
        ],
        "category_id": "27"
    }
    with open(ep_dir / spec["meta_filename"], "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        
    return ep_dir

def render_episode(spec):
    ep_dir = BASE_DIR / spec["folder"]
    neural_dir = ep_dir / "neural_vocals"
    manifest_file = neural_dir / "voice_manifest.json"
    
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    # Calculate timestamps and audio durations
    segments = []
    current_cursor = 0.35
    for item in manifest_data:
        i = item["index"]
        text = item["text"]
        mp3 = neural_dir / f"ana_seg_{i}.mp3"
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(mp3)
        ], capture_output=True, text=True, check=True)
        dur = float(json.loads(res.stdout)["format"]["duration"])
        
        seg_start = round(current_cursor, 3)
        seg_end = round(seg_start + dur, 3)
        
        gap = 1.35 if i == 5 else (0.75 if i in (1, 2) else 0.60)
        segments.append({
            "index": i,
            "text": text,
            "start": seg_start,
            "duration": dur,
            "end": seg_end,
            "wav_path": mp3
        })
        current_cursor = seg_end + gap

    total_duration = round(segments[-1]["end"] + 2.2, 2)
    print(f"⏱️ Episode duration: {total_duration:.2f}s")

    # SFX
    pop_sfx, chime_sfx, boing_sfx = synthesize_cartoon_sfx(ep_dir)
    sfx_dict = {"pop": pop_sfx, "chime": chime_sfx, "boing": boing_sfx}

    # Music
    bg_music = ep_dir / "preview_melody.wav"
    if not bg_music.exists():
        src_music = BASE_DIR / "episodes/Ep_026_Letter_Z/preview_melody.wav"
        shutil.copyfile(str(src_music), str(bg_music))

    # Soundtrack
    final_audio = ep_dir / "soundtrack_with_vocals.wav"
    build_complete_audio(segments, sfx_dict, bg_music, final_audio, total_duration=total_duration)

    # Subtitles
    theme = SUBTITLE_THEMES[0]
    for fmt in ["landscape", "shorts"]:
        ass_path = ep_dir / f"animated_subtitles_{fmt}.ass"
        generate_animated_ass_subtitles(segments, theme, ass_path, is_shorts=(fmt == "shorts"), letter="ABC", char_name="Friends", obj_name="Zoo")

    # Spotlight
    generate_interactive_spotlight_png(ep_dir / "spotlight_pointer.png")

    # HyperFrames Render
    print(f"🚀 Rendering LANDSCAPE for {ep_dir.name}...")
    render_episode_with_hyperframes(ep_dir, output_format="landscape", quality="looks", fps=60)
    print(f"🚀 Rendering SHORTS for {ep_dir.name}...")
    render_episode_with_hyperframes(ep_dir, output_format="shorts", quality="looks", fps=30)
    print(f"🎉 Completed rendering {ep_dir.name}!")

def update_schedule_state():
    state_file = BASE_DIR / "schedule_state.json"
    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    # Find highest video counter
    existing_ids = [int(item["id"][1:]) for item in state["queue"]]
    next_counter = max(existing_ids) + 1 if existing_ids else 53

    for spec in SPECIAL_EPISODES:
        day = spec["day"]
        # Check if already in queue
        if any(item["day"] == day for item in state["queue"]):
            continue

        id_m = f"V{next_counter:03d}"
        next_counter += 1
        id_e = f"V{next_counter:03d}"
        next_counter += 1

        state["queue"].append({
            "id": id_m,
            "day": day,
            "slot": "morning_8am",
            "publish_at_ist": spec["date_ist_morning"],
            "publish_at_utc": spec["date_utc_morning"],
            "episode_dir": spec["folder"],
            "letter": spec["badge"],
            "format": "landscape",
            "playlist_id": "PLK8H9ffAc9HcY7cafr91S1k3bsZnRB3Xc", # ABC learning Video
            "status": "pending",
            "youtube_id": None
        })

        state["queue"].append({
            "id": id_e,
            "day": day,
            "slot": "evening_5pm",
            "publish_at_ist": spec["date_ist_evening"],
            "publish_at_utc": spec["date_utc_evening"],
            "episode_dir": spec["folder"],
            "letter": spec["badge"],
            "format": "shorts",
            "playlist_id": "PLK8H9ffAc9HcZLLbDSmLrz19WxjNwC0-J", # ✨Shorts✨
            "status": "pending",
            "youtube_id": None
        })

    state["total_queued"] = len(state["queue"])
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print(f"✅ Updated schedule_state.json with Days 27, 28, 29! Total queued: {state['total_queued']}")

def main():
    print("🎬 Starting Special Episodes Pipeline for Days 27, 28, 29...")
    for spec in SPECIAL_EPISODES:
        print(f"\n========================================\nSetting up {spec['folder']}...\n========================================")
        setup_episode(spec)
        print(f"Rendering {spec['folder']}...")
        render_episode(spec)

    print("\nUpdating schedule state...")
    update_schedule_state()
    print("🎉 All 3 special episodes produced and added to schedule queue!")

if __name__ == "__main__":
    main()
