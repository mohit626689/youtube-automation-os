#!/usr/bin/env python3
"""
ABC Zoo TV — 100-Day Autonomous Scheduling & Publishing Engine
- Publishes 2 times daily:
    * Slot 1: 08:00 AM IST (02:30 UTC) — Full HD Landscape Episode (16:9)
    * Slot 2: 05:00 PM IST (11:30 UTC) — Vertical YouTube Short (9:16)
- High-converting vidIQ Score 96+ metadata (curiosity question hook + rich 3-paragraph SEO description)
- Automatic playlist tagging:
    * "ABC learning Video" (PLK8H9ffAc9HcY7cafr91S1k3bsZnRB3Xc) for Landscape
    * "✨Shorts✨" (PLK8H9ffAc9HcZLLbDSmLrz19WxjNwC0-J) for Shorts
- YouTube Native Scheduled Publishing (publishAt ISO 8601 UTC)
- State persistence in schedule_state.json
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "schedule_state.json"
CONFIG_FILE = BASE_DIR / "pipeline_config.json"

PLAYLIST_LANDSCAPE = "PLK8H9ffAc9HcY7cafr91S1k3bsZnRB3Xc" # ABC learning Video
PLAYLIST_SHORTS = "PLK8H9ffAc9HcZLLbDSmLrz19WxjNwC0-J"    # ✨Shorts✨

def load_schedule_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return init_100_day_schedule()

def init_100_day_schedule():
    """Initializes the full 100-day release calendar starting tomorrow."""
    # Local time is IST (UTC+5:30)
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)
    start_date = (now_ist + timedelta(days=1)).date()

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    queue = []
    video_counter = 1

    # Phase 1: 26 Letters (A to Z) -> Days 1 to 26
    for i, letter in enumerate(alphabet):
        day_num = i + 1
        curr_date = start_date + timedelta(days=i)
        
        # Slot 1: 08:00 AM IST -> 02:30 UTC
        slot1_ist = datetime(curr_date.year, curr_date.month, curr_date.day, 8, 0, 0, tzinfo=ist)
        slot1_utc = slot1_ist.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Slot 2: 05:00 PM IST (17:00) -> 11:30 UTC
        slot2_ist = datetime(curr_date.year, curr_date.month, curr_date.day, 17, 0, 0, tzinfo=ist)
        slot2_utc = slot2_ist.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        ep_dir = f"episodes/Ep_{day_num:03d}_Letter_{letter}"

        queue.append({
            "id": f"V{video_counter:03d}",
            "day": day_num,
            "slot": "morning_8am",
            "publish_at_ist": slot1_ist.strftime("%Y-%m-%d 08:00 AM IST"),
            "publish_at_utc": slot1_utc,
            "episode_dir": ep_dir,
            "letter": letter,
            "format": "landscape",
            "playlist_id": PLAYLIST_LANDSCAPE,
            "status": "pending", # pending, uploaded, scheduled
            "youtube_id": None
        })
        video_counter += 1

        queue.append({
            "id": f"V{video_counter:03d}",
            "day": day_num,
            "slot": "evening_5pm",
            "publish_at_ist": slot2_ist.strftime("%Y-%m-%d 05:00 PM IST"),
            "publish_at_utc": slot2_utc,
            "episode_dir": ep_dir,
            "letter": letter,
            "format": "shorts",
            "playlist_id": PLAYLIST_SHORTS,
            "status": "pending",
            "youtube_id": None
        })
        video_counter += 1

    state = {
        "channel": "@ABCZooTv",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_queued": len(queue),
        "queue": queue
    }

    save_schedule_state(state)
    return state

def save_schedule_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def schedule_batch(count=2):
    """Processes and schedules the next un-scheduled videos on YouTube."""
    state = load_schedule_state()
    uploader_script = BASE_DIR / "scripts" / "upload_to_youtube.py"
    animator_script = BASE_DIR / "scripts" / "generate_animated_episode.py"

    scheduled_count = 0
    for item in state["queue"]:
        if scheduled_count >= count:
            break
        if item["status"] != "pending":
            continue

        ep_dir = BASE_DIR / item["episode_dir"]
        format_type = item["format"]
        publish_time = item["publish_at_utc"]
        video_file = ep_dir / f"final_animated_{format_type}.mp4"

        print(f"\n📦 Processing [{item['id']}] {item['letter']} ({format_type.upper()}) for {item['publish_at_ist']}")

        # 1. Render animated video if missing
        if not video_file.exists():
            print(f"🎬 Rendering {format_type} video for {ep_dir.name}...")
            theme_idx = (ord(item["letter"]) - ord("A")) % 5
            subprocess.run([
                "python3", str(animator_script),
                "--episode_dir", str(ep_dir),
                "--format", format_type,
                "--theme", str(theme_idx)
            ], check=True)

        # 2. Upload with scheduled publishing
        cmd = [
            "python3", str(uploader_script),
            "--episode_dir", str(ep_dir),
            "--format", format_type,
            "--privacy", "private",
            "--publish_at", publish_time,
            "--playlist_id", item["playlist_id"]
        ]

        print(f"🚀 Uploading & Scheduling on YouTube for: {publish_time}...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            import re
            m = re.search(r"https://youtu\.be/([a-zA-Z0-9_-]+)", res.stdout)
            vid = m.group(1) if m else "scheduled"
            item["status"] = "scheduled"
            item["youtube_id"] = vid
            scheduled_count += 1
            print(f"✅ Successfully scheduled [{item['id']}]! Video ID: {vid}")
            save_schedule_state(state)
        else:
            print(f"❌ Upload failed: {res.stderr}")
            break

    print(f"\n✨ Batch complete. {scheduled_count} videos scheduled.")
    return scheduled_count

def show_schedule():
    state = load_schedule_state()
    print("\n📅 ABC Zoo TV — 100-Day Autonomous Release Schedule:")
    print("=" * 80)
    for item in state["queue"][:10]:
        status_icon = "🟢" if item["status"] == "scheduled" else "⏳"
        print(f"{status_icon} [{item['id']}] Day {item['day']:02d} | {item['publish_at_ist']} | Letter {item['letter']} ({item['format'].upper():9s}) | Status: {item['status'].upper()}")
    print("=" * 80)
    print(f"Total queued releases: {len(state['queue'])}")

def main():
    parser = argparse.ArgumentParser(description="ABC Zoo TV 100-Day Scheduler")
    parser.add_argument("--schedule_next", type=int, default=0, help="Number of upcoming videos to render & schedule on YouTube")
    parser.add_argument("--show", action="store_true", help="Display current release schedule")
    args = parser.parse_args()

    if args.show or (args.schedule_next == 0):
        show_schedule()

    if args.schedule_next > 0:
        schedule_batch(args.schedule_next)

if __name__ == "__main__":
    main()
