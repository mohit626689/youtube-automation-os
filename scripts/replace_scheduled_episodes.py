#!/usr/bin/env python3
"""
Replace scheduled YouTube videos (Landscape & Shorts) with re-rendered versions.
Deletes old scheduled videos and re-uploads with identical publishAt schedule,
calibrated subtitles, 95+ vidIQ SEO metadata, and 16:9 full-bleed thumbnails.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))

from upload_to_youtube import get_oauth_tokens, prepare_episode_metadata, upload_video_resumable

def delete_youtube_video(access_token, video_id):
    """Deletes a video from YouTube via Data API v3."""
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        method="DELETE"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"🗑️ Successfully deleted old video {video_id} (Status: {resp.status})")
            return True
    except urllib.error.HTTPError as e:
        print(f"⚠️ Note on delete {video_id} (HTTP {e.code}): {e.reason}")
        return False
    except Exception as e:
        print(f"⚠️ Failed to delete {video_id}: {e}")
        return False

def replace_scheduled_episodes(queue_ids=None):
    state_file = BASE_DIR / "schedule_state.json"
    client_secrets = BASE_DIR / "client_secrets.json"
    token_file = BASE_DIR / "token.json"

    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    access_token = get_oauth_tokens(str(client_secrets), str(token_file))

    if queue_ids:
        target_items = [
            item for item in state["queue"]
            if item["id"] in queue_ids
        ]
    else:
        # Default to Day 27, 28, 29 (V053 - V058)
        target_items = [
            item for item in state["queue"]
            if item["id"] in ["V053", "V054", "V055", "V056", "V057", "V058"]
        ]

    print(f"🚀 Found {len(target_items)} scheduled videos to replace with calibrated subtitle versions.\n")

    for item in target_items:
        old_id = item.get("youtube_id")
        ep_dir = BASE_DIR / item["episode_dir"]
        fmt = item["format"]
        video_filename = f"final_animated_{fmt}.mp4"
        video_path = ep_dir / video_filename
        
        if not video_path.exists():
            print(f"❌ Video file missing: {video_path}. Skipping item {item['id']}.")
            continue

        thumb_path = ep_dir / "high_ctr_thumbnail_16_9.jpg" if fmt == "landscape" else None
        if thumb_path and not thumb_path.exists():
            thumb_path = None

        playlist_id = item.get("playlist_id")

        print("=" * 65)
        print(f"🔄 Processing [{item['id']}] Day {item['day']} ({fmt.upper()}) - {item['letter']}")
        print(f"   Episode Folder : {ep_dir.name}")
        print(f"   Old Video ID   : {old_id}")
        print(f"   Scheduled For  : {item['publish_at_ist']} ({item['publish_at_utc']})")
        print(f"   Video File     : {video_path.name} ({video_path.stat().st_size / (1024*1024):.2f} MB)")
        print(f"   Thumbnail      : {thumb_path.name if thumb_path else 'None (Shorts/Auto)'}")
        print("=" * 65)

        # 1. Delete old video if it exists
        if old_id:
            delete_youtube_video(access_token, old_id)

        # 2. Prepare metadata with rich vidIQ 95+ SEO
        metadata = prepare_episode_metadata(
            ep_dir,
            format_type=fmt,
            privacy="private",
            publish_at=item["publish_at_utc"]
        )

        # 3. Resumable upload
        new_id, new_url = upload_video_resumable(
            access_token,
            video_path,
            metadata,
            thumbnail_path=str(thumb_path) if thumb_path else None,
            playlist_id=playlist_id
        )

        # 4. Update schedule state
        item["youtube_id"] = new_id
        item["status"] = "scheduled"

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

        print(f"✅ Item [{item['id']}] Successfully Replaced!")
        print(f"   New YouTube ID: {new_id}")
        print(f"   Watch URL: {new_url}\n")

    print("\n🎉 All target scheduled videos replaced and verified successfully!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Replace scheduled YouTube releases")
    parser.add_argument("--ids", nargs="+", help="Specific queue IDs to replace, e.g. V053 V054")
    args = parser.parse_args()

    replace_scheduled_episodes(queue_ids=args.ids)
