#!/usr/bin/env python3
"""
Schedule Day 30 (Ep_030_Wash_Hands) on YouTube for both Landscape and Shorts.
Applies:
- High-CTR 16:9 thumbnail
- 95+ vidIQ rich SEO description and metadata
- Scheduled release timestamps for October 24, 2026 (Morning 8 AM & Evening 5 PM IST)
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))

from upload_to_youtube import get_oauth_tokens, prepare_episode_metadata, upload_video_resumable

def schedule_day_30():
    state_file = BASE_DIR / "schedule_state.json"
    client_secrets = BASE_DIR / "client_secrets.json"
    token_file = BASE_DIR / "token.json"

    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    access_token = get_oauth_tokens(str(client_secrets), str(token_file))
    ep_dir = BASE_DIR / "episodes/Ep_030_Wash_Hands"

    releases = [
        {
            "id": "V059",
            "day": 30,
            "slot": "morning_8am",
            "publish_at_ist": "2026-10-24 08:00 AM IST",
            "publish_at_utc": "2026-10-24T02:30:00Z",
            "episode_dir": "episodes/Ep_030_Wash_Hands",
            "letter": "WASH HANDS",
            "format": "landscape",
            "playlist_id": "PLK8H9ffAc9HcY7cafr91S1k3bsZnRB3Xc",
            "video_path": ep_dir / "final_animated_landscape.mp4",
            "thumbnail_path": ep_dir / "high_ctr_thumbnail_16_9.jpg"
        },
        {
            "id": "V060",
            "day": 30,
            "slot": "evening_5pm",
            "publish_at_ist": "2026-10-24 05:00 PM IST",
            "publish_at_utc": "2026-10-24T11:30:00Z",
            "episode_dir": "episodes/Ep_030_Wash_Hands",
            "letter": "WASH HANDS",
            "format": "shorts",
            "playlist_id": "PLK8H9ffAc9HcZLLbDSmLrz19WxjNwC0-J",
            "video_path": ep_dir / "final_animated_shorts.mp4",
            "thumbnail_path": None
        }
    ]

    print("🚀 Initiating YouTube Upload & Schedule for Day 30...\n")

    for rel in releases:
        print("=" * 70)
        print(f"📦 Scheduling [{rel['id']}] Day {rel['day']} ({rel['format'].upper()})")
        print(f"   Scheduled For : {rel['publish_at_ist']} ({rel['publish_at_utc']})")
        print(f"   Video File    : {rel['video_path'].name} ({rel['video_path'].stat().st_size / (1024*1024):.2f} MB)")
        print(f"   Thumbnail     : {rel['thumbnail_path'].name if rel['thumbnail_path'] else 'Auto (Shorts)'}")
        print("=" * 70)

        metadata = prepare_episode_metadata(
            ep_dir,
            format_type=rel["format"],
            privacy="private",
            publish_at=rel["publish_at_utc"]
        )

        new_id, new_url = upload_video_resumable(
            access_token,
            rel["video_path"],
            metadata,
            thumbnail_path=str(rel["thumbnail_path"]) if rel["thumbnail_path"] else None,
            playlist_id=rel["playlist_id"]
        )

        entry = {
            "id": rel["id"],
            "day": rel["day"],
            "slot": rel["slot"],
            "publish_at_ist": rel["publish_at_ist"],
            "publish_at_utc": rel["publish_at_utc"],
            "episode_dir": rel["episode_dir"],
            "letter": rel["letter"],
            "format": rel["format"],
            "playlist_id": rel["playlist_id"],
            "status": "scheduled",
            "youtube_id": new_id
        }

        # Check if already in queue or append
        existing = [i for i, item in enumerate(state["queue"]) if item["id"] == rel["id"]]
        if existing:
            state["queue"][existing[0]] = entry
        else:
            state["queue"].append(entry)

        state["total_queued"] = len(state["queue"])

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

        print(f"✅ Successfully scheduled [{rel['id']}]! Video ID: {new_id} ({new_url})\n")

    print("🎉 Day 30 (October 24, 2026) fully scheduled on YouTube!")

if __name__ == "__main__":
    schedule_day_30()
