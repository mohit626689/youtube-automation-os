#!/usr/bin/env python3
"""
YouTube Video SEO & High-CTR Thumbnail Updater
Updates video title, description, tags, and uploads native 16:9 thumbnail via YouTube Data API v3.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))
from upload_to_youtube import get_oauth_tokens

def update_video_seo(video_id, title, description, tags, thumbnail_path=None, category_id="27"):
    token = get_oauth_tokens(str(BASE_DIR / "client_secrets.json"), str(BASE_DIR / "token.json"))

    # 1. Update snippet metadata
    print(f"🔄 Updating metadata for video: {video_id}...")
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet"
    payload = {
        "id": video_id,
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": category_id
        }
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="PUT"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode())
            print(f"✅ Successfully updated title & description!")
            print(f"   📌 New Title: {res_data['snippet']['title']}")
    except Exception as e:
        print(f"❌ Failed to update snippet: {e}")
        raise

    # 2. Upload custom 16:9 thumbnail
    if thumbnail_path and os.path.exists(thumbnail_path):
        print(f"🖼️ Uploading high-CTR 16:9 thumbnail: {Path(thumbnail_path).name}...")
        thumb_url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
        with open(thumbnail_path, "rb") as tf:
            thumb_bytes = tf.read()

        thumb_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "image/jpeg",
            "Content-Length": str(len(thumb_bytes))
        }
        thumb_req = urllib.request.Request(thumb_url, data=thumb_bytes, headers=thumb_headers, method="POST")
        try:
            with urllib.request.urlopen(thumb_req) as resp:
                print("✅ Successfully applied new high-CTR 16:9 thumbnail!")
        except Exception as e:
            print(f"⚠️ Note: Custom thumbnail could not be set automatically ({e}).")

    print(f"🔗 Check on YouTube Studio: https://studio.youtube.com/video/{video_id}/edit")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--desc_file", required=True)
    parser.add_argument("--thumbnail", default=None)
    args = parser.parse_args()

    with open(args.desc_file, "r", encoding="utf-8") as f:
        desc = f.read()

    tags = [
        "Best ABC Phonics Song for Kids",
        "Phonics alphabet song",
        "learn A-Z in minutes",
        "learn ABC",
        "preschool learning",
        "kids animation",
        "toddler songs",
        "alphabet songs for children",
        "ABC Zoo TV",
        "phonics songs for kindergarten",
        "learn alphabet",
        "abc song",
        "educational videos for kids",
        "nursery rhymes"
    ]

    update_video_seo(args.video_id, args.title, desc, tags, thumbnail_path=args.thumbnail)
