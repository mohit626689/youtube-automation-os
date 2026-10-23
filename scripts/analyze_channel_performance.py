#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))
from upload_to_youtube import get_oauth_tokens

def analyze_channel():
    token = get_oauth_tokens(str(BASE_DIR / "client_secrets.json"), str(BASE_DIR / "token.json"))

    # 1. Fetch Channel Info
    url = "https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails,statistics&mine=true"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    
    channel = data["items"][0]
    print("=" * 80)
    print("📺 CHANNEL OVERVIEW: ", channel["snippet"]["title"], f"(@{channel['snippet'].get('customUrl', 'ABCZooTv')})")
    print(f"👥 Subscribers : {channel['statistics'].get('subscriberCount', 0)}")
    print(f"👀 Total Views  : {channel['statistics'].get('viewCount', 0)}")
    print(f"🎬 Total Videos : {channel['statistics'].get('videoCount', 0)}")
    print("=" * 80)

    uploads_playlist = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    # 2. Fetch up to 50 items from the uploads playlist
    pl_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={uploads_playlist}&maxResults=50"
    req = urllib.request.Request(pl_url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        pl_data = json.loads(resp.read().decode())

    video_ids = [item["snippet"]["resourceId"]["videoId"] for item in pl_data["items"]]

    # 3. Fetch statistics for these videos in chunks of 50
    ids_str = ",".join(video_ids)
    v_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails,statistics&id={ids_str}"
    req = urllib.request.Request(v_url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        v_data = json.loads(resp.read().decode())

    long_videos = []
    short_videos = []

    for item in v_data["items"]:
        v_id = item["id"]
        snip = item["snippet"]
        stat = item.get("statistics", {})
        status = item.get("status", {})
        title = snip["title"]
        views = int(stat.get("viewCount", "0"))
        likes = int(stat.get("likeCount", "0"))
        comments = int(stat.get("commentCount", "0"))
        privacy = status.get("privacyStatus")
        published_at = snip.get("publishedAt")
        dur = item["contentDetails"]["duration"]
        is_short = "#Shorts" in title or "Shorts" in title or "#shorts" in title or "#Short" in title

        entry = {
            "id": v_id,
            "title": title,
            "views": views,
            "likes": likes,
            "comments": comments,
            "privacy": privacy,
            "published_at": published_at,
            "duration": dur,
            "thumbnails": snip.get("thumbnails", {})
        }
        if is_short:
            short_videos.append(entry)
        else:
            long_videos.append(entry)

    print(f"\n📊 SUMMARY OF RECENT {len(v_data['items'])} VIDEOS ANALYZED:")
    print(f"   Long-form Videos: {len(long_videos)}")
    print(f"   Shorts Videos   : {len(short_videos)}")

    print("\n--- 🟢 TOP LONG-FORM VIDEOS (BY VIEWS) ---")
    long_sorted = sorted(long_videos, key=lambda x: x["views"], reverse=True)
    for v in long_sorted[:10]:
        print(f"👁️ {v['views']:>5} views | 👍 {v['likes']:>2} likes | [{v['privacy']}] | {v['title'][:65]}... (ID: {v['id']})")

    print("\n--- 📱 ALL SHORTS VIDEOS (BY VIEWS) ---")
    shorts_sorted = sorted(short_videos, key=lambda x: x["views"], reverse=True)
    for v in shorts_sorted:
        print(f"👁️ {v['views']:>5} views | 👍 {v['likes']:>2} likes | [{v['privacy']}] | {v['title'][:65]}... (ID: {v['id']})")

    # Aggregate stats
    public_long = [v for v in long_videos if v["privacy"] == "public"]
    public_shorts = [v for v in short_videos if v["privacy"] == "public"]

    avg_long_views = sum(v["views"] for v in public_long) / max(1, len(public_long))
    avg_short_views = sum(v["views"] for v in public_shorts) / max(1, len(public_shorts))

    print("\n📈 AVERAGE PERFORMANCE ON PUBLIC VIDEOS:")
    print(f"   Public Long-form count: {len(public_long)} | Avg Views: {avg_long_views:.1f}")
    print(f"   Public Shorts count    : {len(public_shorts)} | Avg Views: {avg_short_views:.1f}")

if __name__ == "__main__":
    analyze_channel()
