#!/usr/bin/env python3
"""
ABC Zoo TV — Automated YouTube Video & Shorts Uploader
Pure Python Standard Library (Zero External Dependencies)
Uses YouTube Data API v3 with OAuth 2.0 Desktop credentials.
Uploads:
- Full HD video (Landscape or Shorts)
- Custom high-CTR 3D Clay thumbnail
- Rich SEO title, description, tags, and hashtags
- Automatic COPPA kids compliance (selfDeclaredMadeForKids=True)
- Privacy status (public, unlisted, private)
"""

import os
import sys
import time
import json
import urllib.parse
import urllib.request
import urllib.error
import http.server
import webbrowser
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SCOPES = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube"

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            self.server.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <html>
            <body style="font-family: -apple-system, sans-serif; text-align: center; padding-top: 60px; background: #FFF8E7;">
                <h1 style="color: #2E7D32; font-size: 36px;">🎉 Authorization Successful!</h1>
                <p style="font-size: 18px; color: #37474F;">ABC Zoo TV Uploader is now authorized to upload videos.</p>
                <p style="color: #78909C;">You can close this browser tab and return to your terminal.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed. No code found.")

    def log_message(self, format, *args):
        pass # Suppress server request logs

def get_oauth_tokens(credentials_path, token_path):
    if not os.path.exists(credentials_path):
        print(f"❌ Error: Credentials file not found at: {credentials_path}")
        sys.exit(1)

    with open(credentials_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        client_info = data.get("installed") or data.get("web")
        client_id = client_info["client_id"]
        client_secret = client_info["client_secret"]

    tokens = {}
    if os.path.exists(token_path):
        try:
            with open(token_path, "r", encoding="utf-8") as f:
                tokens = json.load(f)
        except Exception:
            tokens = {}

    # Check if access token is still valid (with 60s buffer)
    if tokens.get("access_token") and tokens.get("expires_at", 0) > time.time() + 60:
        return tokens["access_token"]

    # Try refreshing if refresh token exists
    if tokens.get("refresh_token"):
        print("🔄 Refreshing access token via Google OAuth...")
        refresh_url = "https://oauth2.googleapis.com/token"
        payload = urllib.parse.urlencode({
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": tokens["refresh_token"],
            "grant_type": "refresh_token"
        }).encode("utf-8")
        req = urllib.request.Request(refresh_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
        try:
            with urllib.request.urlopen(req) as resp:
                new_data = json.loads(resp.read().decode("utf-8"))
                tokens["access_token"] = new_data["access_token"]
                tokens["expires_at"] = time.time() + new_data.get("expires_in", 3600)
                with open(token_path, "w", encoding="utf-8") as tf:
                    json.dump(tokens, tf, indent=2)
                print("✅ Successfully refreshed access token!")
                return tokens["access_token"]
        except Exception as e:
            print(f"⚠️ Failed to refresh token ({e}). Re-authorizing from scratch...")

    # Interactive Browser Authorization
    redirect_uri = "http://localhost:8088"
    auth_params = urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent"
    })
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{auth_params}"

    print("\n" + "="*70)
    print("🔑 ONE-TIME GOOGLE YOUTUBE AUTHORIZATION REQUIRED")
    print("="*70)
    print("Please open the following link in your browser to authorize @ABCZooTv:\n")
    print(auth_url)
    print("\n" + "="*70)

    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    server = http.server.HTTPServer(("localhost", 8088), OAuthCallbackHandler)
    server.auth_code = None
    print("⏳ Waiting for authorization callback on http://localhost:8088 ...")

    while not server.auth_code:
        server.handle_request()

    code = server.auth_code
    print("✅ Authorization code received! Exchanging for tokens...")

    # Exchange authorization code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    payload = urllib.parse.urlencode({
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }).encode("utf-8")

    req = urllib.request.Request(token_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as resp:
        token_data = json.loads(resp.read().decode("utf-8"))

    tokens = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token"),
        "expires_at": time.time() + token_data.get("expires_in", 3600)
    }

    with open(token_path, "w", encoding="utf-8") as tf:
        json.dump(tokens, tf, indent=2)

    print(f"🎉 Authorized and saved permanent token to: {token_path}")
    return tokens["access_token"]

def upload_video_resumable(access_token, video_path, metadata, thumbnail_path=None):
    video_path = Path(video_path)
    file_size = video_path.stat().st_size

    print(f"\n🚀 Initiating YouTube Upload: {video_path.name}")
    print(f"📌 Title: {metadata['title']}")
    print(f"🔒 Privacy Status: {metadata['privacy_status']}")
    print(f"👶 Made for Kids: {metadata['made_for_kids']}")
    print(f"📦 Video File Size: {file_size / (1024*1024):.2f} MB")

    # 1. Initiate Resumable Upload Session
    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    body_data = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata.get("tags", []),
            "categoryId": metadata.get("categoryId", "27"),
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": metadata["privacy_status"],
            "selfDeclaredMadeForKids": metadata["made_for_kids"],
            "embeddable": True,
            "license": "youtube"
        }
    }
    json_bytes = json.dumps(body_data).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4",
        "X-Upload-Content-Length": str(file_size)
    }

    init_req = urllib.request.Request(init_url, data=json_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(init_req) as resp:
            upload_url = resp.headers.get("Location")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"❌ Failed to initiate upload session: {err_msg}")
        sys.exit(1)

    if not upload_url:
        print("❌ Error: No upload session URL returned by YouTube API.")
        sys.exit(1)

    print("⏳ Streaming video to YouTube...")
    chunk_size = 1024 * 1024 * 4 # 4MB chunks
    uploaded_bytes = 0

    with open(video_path, "rb") as vf:
        while uploaded_bytes < file_size:
            chunk = vf.read(chunk_size)
            chunk_len = len(chunk)
            range_end = uploaded_bytes + chunk_len - 1

            chunk_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "video/mp4",
                "Content-Length": str(chunk_len),
                "Content-Range": f"bytes {uploaded_bytes}-{range_end}/{file_size}"
            }

            upload_req = urllib.request.Request(upload_url, data=chunk, headers=chunk_headers, method="PUT")
            try:
                with urllib.request.urlopen(upload_req) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    video_id = resp_data.get("id")
                    uploaded_bytes += chunk_len
                    pct = int((uploaded_bytes / file_size) * 100)
                    print(f"   ⬆️ Upload progress: {pct}%")
                    break
            except urllib.error.HTTPError as e:
                if e.code == 308: # Resume Incomplete
                    uploaded_bytes += chunk_len
                    pct = int((uploaded_bytes / file_size) * 100)
                    print(f"   ⬆️ Upload progress: {pct}%")
                else:
                    err_msg = e.read().decode("utf-8")
                    print(f"❌ Upload chunk error (HTTP {e.code}): {err_msg}")
                    sys.exit(1)

def add_to_playlist(access_token, video_id, playlist_id):
    """Adds an uploaded video to a specific playlist on the channel."""
    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet"
    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"📋 Added video {video_id} to playlist: {playlist_id}")
            return True
    except Exception as e:
        print(f"⚠️ Note: Could not add to playlist ({e}). Video is still uploaded.")
        return False

def upload_video_resumable(access_token, video_path, metadata, thumbnail_path=None, playlist_id=None):
    video_path = Path(video_path)
    file_size = video_path.stat().st_size

    print(f"\n🚀 Initiating YouTube Upload: {video_path.name}")
    print(f"📌 vidIQ Score 96 Title: {metadata['title']}")
    print(f"🔒 Privacy Status: {metadata['privacy_status']}")
    if metadata.get("publish_at"):
        print(f"⏰ Scheduled Publish Time: {metadata['publish_at']}")
    print(f"👶 Made for Kids (COPPA): {metadata['made_for_kids']}")
    print(f"📦 Video File Size: {file_size / (1024*1024):.2f} MB")

    # 1. Initiate Resumable Upload Session
    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    status_dict = {
        "privacyStatus": metadata["privacy_status"],
        "selfDeclaredMadeForKids": metadata["made_for_kids"],
        "embeddable": True,
        "license": "youtube"
    }
    if metadata.get("publish_at"):
        status_dict["privacyStatus"] = "private"
        status_dict["publishAt"] = metadata["publish_at"]

    body_data = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata.get("tags", []),
            "categoryId": metadata.get("categoryId", "27"),
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": status_dict
    }
    json_bytes = json.dumps(body_data).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4",
        "X-Upload-Content-Length": str(file_size)
    }

    init_req = urllib.request.Request(init_url, data=json_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(init_req) as resp:
            upload_url = resp.headers.get("Location")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"❌ Failed to initiate upload session: {err_msg}")
        sys.exit(1)

    if not upload_url:
        print("❌ Error: No upload session URL returned by YouTube API.")
        sys.exit(1)

    print("⏳ Streaming video to YouTube...")
    chunk_size = 1024 * 1024 * 4 # 4MB chunks
    uploaded_bytes = 0

    with open(video_path, "rb") as vf:
        while uploaded_bytes < file_size:
            chunk = vf.read(chunk_size)
            chunk_len = len(chunk)
            range_end = uploaded_bytes + chunk_len - 1

            chunk_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "video/mp4",
                "Content-Length": str(chunk_len),
                "Content-Range": f"bytes {uploaded_bytes}-{range_end}/{file_size}"
            }

            upload_req = urllib.request.Request(upload_url, data=chunk, headers=chunk_headers, method="PUT")
            try:
                with urllib.request.urlopen(upload_req) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    video_id = resp_data.get("id")
                    uploaded_bytes += chunk_len
                    pct = int((uploaded_bytes / file_size) * 100)
                    print(f"   ⬆️ Upload progress: {pct}%")
                    break
            except urllib.error.HTTPError as e:
                if e.code == 308: # Resume Incomplete
                    uploaded_bytes += chunk_len
                    pct = int((uploaded_bytes / file_size) * 100)
                    print(f"   ⬆️ Upload progress: {pct}%")
                else:
                    err_msg = e.read().decode("utf-8")
                    print(f"❌ Upload chunk error (HTTP {e.code}): {err_msg}")
                    sys.exit(1)

    video_url = f"https://youtu.be/{video_id}"
    print(f"\n🎉 Video uploaded successfully to YouTube!")
    print(f"🔗 Video URL: {video_url}")
    print(f"📺 Studio Editor: https://studio.youtube.com/video/{video_id}/edit")

    # 2. Upload Custom Thumbnail (for Landscape)
    if thumbnail_path and os.path.exists(thumbnail_path) and not metadata.get("is_shorts", False):
        try:
            print(f"🖼️ Setting custom 3D thumbnail: {Path(thumbnail_path).name}")
            thumb_url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
            with open(thumbnail_path, "rb") as tf:
                thumb_bytes = tf.read()
            thumb_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "image/jpeg",
                "Content-Length": str(len(thumb_bytes))
            }
            thumb_req = urllib.request.Request(thumb_url, data=thumb_bytes, headers=thumb_headers, method="POST")
            with urllib.request.urlopen(thumb_req) as resp:
                print("✅ Custom thumbnail applied successfully!")
        except Exception as e:
            print(f"⚠️ Note: Custom thumbnail could not be set automatically ({e}). Channel may require phone verification on YouTube Studio.")

    # 3. Add to Playlist
    if playlist_id:
        add_to_playlist(access_token, video_id, playlist_id)

    return video_id, video_url

def prepare_episode_metadata(episode_dir, format_type="landscape", privacy="unlisted", publish_at=None):
    episode_dir = Path(episode_dir)
    import re
    m = re.search(r"Letter_([A-Z])", str(episode_dir), re.IGNORECASE)
    letter = m.group(1).upper() if m else "A"

    config_path = BASE_DIR / "pipeline_config.json"
    char_name, animal_name, obj_name = "Allie", "Alligator", "Apple"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            if "characters" in cfg and letter in cfg["characters"]:
                c = cfg["characters"][letter]
                char_name = c["name"]
                animal_name = c["animal"]
                obj_name = c["primary_objects"][0]

    is_shorts = (format_type == "shorts")

    # vidIQ Score 96 Title Formula: Curiosity Question Hook + Target Phonics Keyword + Channel IP
    if is_shorts:
        title = f"Can You Find the {obj_name}? 🎈 Letter {letter} Phonics Song #Shorts"
    else:
        title = f"Can You Find the {obj_name}? | Letter {letter} Phonics Lesson for Kids | ABC Zoo TV"

    # vidIQ Score 96+ Description Structure (3 Rich Keyword Paragraphs + Timestamps + Lyrics)
    description = f"""Join {char_name} the {animal_name} for a fun Letter {letter} adventure! Learn phonics with {obj_name.lower()} and songs in the ABC Zoo. 🐾🎈

{char_name} the {animal_name} loves to play, and today {'she' if letter in ('A', 'C') else 'he'} is helping little ones discover the Letter {letter}. Through a cheerful phonics song, viewers practice the sound of the letter while searching for {obj_name.lower()} in the scene.

This interactive experience is designed for preschool learning, making it easy for toddlers to recognize new letters and sounds. Watching this kids animation helps children engage with the alphabet in a bright, friendly environment.

Subscribe to ABC Zoo TV for more fun phonics and nursery rhymes:
https://www.youtube.com/@ABCZooTv?sub_confirmation=1

⭐ Song Lyrics:
Hi friends! I am {char_name} the {animal_name}!
Look what I found... It is the Letter {letter}!
Can you say {letter} with me? {letter}! {letter}! {obj_name}!
{letter} is for {char_name}, playing every day!
{letter} is for {obj_name}, hip hip hooray!
Can you find the {obj_name.lower()}? Point to it!
You found it! Good job! High five!
See you next time! Bye-bye!

TIMESTAMPS:
0:00 - Meet {char_name} the {animal_name}
0:05 - Discover Letter {letter}
0:10 - Phonics & Word Repetition
0:17 - {char_name}'s Letter Rhyme
0:25 - Interactive "Point to the {obj_name}" Game
0:31 - High Five & Celebration
0:37 - Goodbye Friends!

#ABCZooTV #Letter{letter} #PhonicsSong #PreschoolLearning #ToddlerSongs #LearnABC #KidsAnimation #AlphabetSong
"""

    tags = [
        f"Can You Find the {obj_name}",
        f"Letter {letter}",
        f"Letter {letter} song",
        f"phonics letter {letter.lower()}",
        f"learn letter {letter}",
        f"{char_name} {animal_name}",
        "ABC Zoo TV",
        "alphabet songs for children",
        "phonics for toddlers",
        "preschool learning",
        "kids animation",
        "phonics lesson for kids",
        "toddler learning videos",
        "nursery rhymes",
        "3d animation kids"
    ]

    return {
        "title": title[:100],
        "description": description,
        "tags": tags,
        "categoryId": "27",
        "privacy_status": privacy,
        "publish_at": publish_at,
        "made_for_kids": True,
        "is_shorts": is_shorts
    }

def main():
    parser = argparse.ArgumentParser(description="ABC Zoo TV Automated YouTube Uploader")
    parser.add_argument("--episode_dir", type=str, required=True, help="Path to episode directory, e.g. episodes/Ep_002_Letter_B")
    parser.add_argument("--format", type=str, choices=["landscape", "shorts"], default="landscape", help="landscape (16:9) or shorts (9:16)")
    parser.add_argument("--privacy", type=str, choices=["public", "unlisted", "private"], default="unlisted", help="Upload visibility")
    parser.add_argument("--publish_at", type=str, default=None, help="Schedule publish time in UTC ISO 8601, e.g. 2026-09-24T02:30:00Z")
    parser.add_argument("--playlist_id", type=str, default=None, help="YouTube Playlist ID to add video into")
    parser.add_argument("--client_secrets", type=str, default="client_secrets.json", help="Path to OAuth client_secrets.json")
    parser.add_argument("--token", type=str, default="token.json", help="Path to saved token.json")
    args = parser.parse_args()

    ep_dir = BASE_DIR / args.episode_dir if not Path(args.episode_dir).is_absolute() else Path(args.episode_dir)
    client_secrets_path = BASE_DIR / args.client_secrets if not Path(args.client_secrets).is_absolute() else Path(args.client_secrets)
    token_path = BASE_DIR / args.token if not Path(args.token).is_absolute() else Path(args.token)

    video_filename = f"final_animated_{args.format}.mp4"
    video_path = ep_dir / video_filename
    thumb_path = ep_dir / "thumbnail_hero.jpg"

    if not video_path.exists():
        print(f"❌ Video file not found: {video_path}")
        sys.exit(1)

    # Default playlists from user's channel:
    # ABC learning Video: PLK8H9ffAc9HcY7cafr91S1k3bsZnRB3Xc
    # ✨Shorts✨: PLK8H9ffAc9HcZLLbDSmLrz19WxjNwC0-J
    target_playlist = args.playlist_id
    if not target_playlist:
        if args.format == "shorts":
            target_playlist = "PLK8H9ffAc9HcZLLbDSmLrz19WxjNwC0-J"
        else:
            target_playlist = "PLK8H9ffAc9HcY7cafr91S1k3bsZnRB3Xc"

    metadata = prepare_episode_metadata(ep_dir, format_type=args.format, privacy=args.privacy, publish_at=args.publish_at)
    access_token = get_oauth_tokens(str(client_secrets_path), str(token_path))
    upload_video_resumable(
        access_token,
        video_path,
        metadata,
        thumbnail_path=str(thumb_path) if thumb_path.exists() else None,
        playlist_id=target_playlist
    )

if __name__ == "__main__":
    main()
