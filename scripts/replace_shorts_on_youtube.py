#!/usr/bin/env python3
"""
Replace all scheduled YouTube Shorts with the newly rendered 9:16 vertical videos.
Deletes old cropped versions from YouTube and uploads new crisp triple-tier Shorts.
"""

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

def replace_all_shorts():
    state_file = BASE_DIR / "schedule_state.json"
    client_secrets = BASE_DIR / "client_secrets.json"
    token_file = BASE_DIR / "token.json"

    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    access_token = get_oauth_tokens(str(client_secrets), str(token_file))

    shorts_items = [
        item for item in state["queue"]
        if item["format"] == "shorts" and item["status"] in ("scheduled", "uploaded_unlisted") and item.get("youtube_id")
    ]

    print(f"Found {len(shorts_items)} Shorts to replace with pristine 9:16 vertical videos.\n")

    for item in shorts_items:
        old_id = item["youtube_id"]
        ep_dir = BASE_DIR / item["episode_dir"]
        video_path = ep_dir / "final_animated_shorts.mp4"
        playlist_id = item.get("playlist_id", "PLK8H9ffAc9HcZLLbDSmLrz19WxjNwC0-J")

        print(f"=======================================================")
        print(f"🔄 Replacing [{item['id']}] Letter {item['letter']} Shorts ({ep_dir.name})")
        print(f"   Old Video ID: {old_id}")
        print(f"   Scheduled for: {item['publish_at_ist']}")
        print(f"=======================================================")

        # Step 1: Delete old video
        delete_youtube_video(access_token, old_id)

        # Step 2: Prepare metadata
        metadata = prepare_episode_metadata(
            ep_dir,
            format_type="shorts",
            privacy="private",
            publish_at=item["publish_at_utc"]
        )

        # Step 3: Upload new 9:16 video
        new_id, new_url = upload_video_resumable(
            access_token,
            video_path,
            metadata,
            thumbnail_path=None,
            playlist_id=playlist_id
        )

        # Step 4: Update state
        item["youtube_id"] = new_id
        item["status"] = "scheduled"
        print(f"✅ Successfully replaced! New Video ID: {new_id} ({new_url})\n")

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    print("🎉 All scheduled Shorts have been successfully replaced on YouTube!")

if __name__ == "__main__":
    replace_all_shorts()
