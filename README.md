# 🌟 Universal YouTube Video Automation Operating System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-6.0+-007808?style=flat&logo=ffmpeg&logoColor=white)](https://ffmpeg.org)
[![Edge-TTS](https://img.shields.io/badge/Edge--TTS-400+_Voices-0078D4?style=flat)](https://github.com/rany2/edge-tts)
[![YouTube API](https://img.shields.io/badge/YouTube_API-v3_OAuth2-FF0000?style=flat&logo=youtube&logoColor=white)](https://developers.google.com/youtube/v3)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An autonomous, broadcast-grade YouTube channel automation operating system designed to run **any YouTube niche** hands-free for 100+ days:
- 🧸 **Preschool & Kids Animation** (3D Clay-Pixar style, sweet child voice)
- 💰 **Faceless Wealth & Finance Documentaries** (Cinematic luxury dark aesthetic, deep narrator)
- 🏛️ **Stoic Philosophy & Motivation** (Ancient Greek marble statue aesthetic, powerful voice)
- 🕯️ **Horror & True Crime / Creepypasta** (Eerie analog VHS aesthetic, chilling narrator)
- ⚡ **Tech & AI Explainers** (Cyberpunk neon aesthetic, modern tech voice)
- 🎯 **Custom Niche / Model from Competitor Channel URL**

---

## 🌟 Key Features

1. **Interactive Setup Wizard (`setup.py`):**
   - Automatically asks for your channel niche or competitor channel URL.
   - Generates your custom `pipeline_config.json`, `channel_brand_bible.md`, and 100-video roadmap.
2. **400+ Authentic Neural Voices (Microsoft Edge TTS):**
   - Zero robotic artifacts or artificial pitch shifts. Authentic emotional range across ages and languages.
3. **Dynamic Sequential Video Compositor (`generate_animated_episode.py`):**
   - **Zero Voice Overlaps:** Probes audio duration with `ffprobe` and dynamically chains lines with natural breathing pauses.
   - **Zero Subtitle Collisions:** Advanced SubStation Alpha (`.ass`) animated typography with strict display clearance.
   - **Synchronized Cartoon / Cinematic SFX:** Audio cues (chimes, pops, whooshes, impacts) lock dynamically to spoken words.
   - **10 Rotational Subtitle Design Themes:** Dynamic font rotating (`Chalkboard SE`, `Arial Rounded MT Bold`, `Marker Felt`, `Comic Sans MS`, `Arial Black`).
4. **vidIQ Score 96+ High-Converting Metadata (`upload_to_youtube.py`):**
   - Question-hook titles (`Can You Find the {Object}? | ...`)
   - 3-paragraph keyword-rich descriptions for maximum search discovery.
   - Automatic routing into channel playlists (`ABC learning Video`, `✨Shorts✨`, etc.).
5. **100-Day Autonomous Cloud Scheduler (`autonomous_100_days_scheduler.py`):**
   - 2 uploads daily (08:00 AM & 05:00 PM) scheduled natively via YouTube's cloud servers (`publishAt`).
   - Runs on autopilot even when your computer is turned off.

---

## 🚀 Quickstart Guide (5-Minute Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/mohit626689/youtube-automation-os.git
cd youtube-automation-os
```

### 2. Install Dependencies
* **Python 3.10+**
* **FFmpeg** (with `libass` and `libfreetype`):
  ```bash
  # macOS
  brew install ffmpeg

  # Ubuntu/Debian
  sudo apt install ffmpeg
  ```
* **Node.js 18+**:
  ```bash
  npm install
  ```

### 3. Run the Interactive Channel Wizard
```bash
python3 setup.py
# Or: npm run setup
```
Select your niche (Kids, Finance, Stoic, Horror, Tech, or Custom). The wizard automatically configures your brand bible and prompt engine!

### 4. Configure YouTube API (One-Time Setup)
1. Go to [Google Cloud Console](https://console.cloud.google.com/) and enable **YouTube Data API v3**.
2. Under **Credentials**, create an **OAuth 2.0 Client ID (Desktop App)**.
3. Copy `client_secrets.example.json` to `client_secrets.json` and paste your `client_id` and `client_secret`:
   ```bash
   cp client_secrets.example.json client_secrets.json
   ```

### 5. Render & Auto-Upload
```bash
# Render both Landscape (16:9) and Shorts (9:16)
python3 scripts/generate_animated_episode.py --episode_dir "episodes/Ep_001" --format both

# Upload directly to YouTube (or Unlisted for review)
python3 scripts/upload_to_youtube.py --episode_dir "episodes/Ep_001" --format landscape --privacy unlisted

# Schedule the 100-day autonomous queue (8 AM & 5 PM daily)
python3 scripts/autonomous_100_days_scheduler.py --schedule_next 2
```

---

## 📁 Repository Structure

```
├── setup.py                          # 1-Click Universal Onboarding Wizard
├── pipeline_config.json              # Master channel engine configuration
├── channel_brand_bible.md            # Visual style tokens & sonic branding
├── 100_video_roadmap.md              # 4-Phase 100-video sequential roadmap
├── kids_script_template.md           # 5-Scene high-retention script formula
├── client_secrets.example.json       # Sanitized OAuth credentials template
├── SKILL.md                          # Official Antigravity Agent Skill specification
└── scripts/
    ├── setup_channel.py              # Interactive niche & competitor channel analyzer
    ├── generate_neural_child_voice.js # Neural voice synthesis engine (Edge TTS)
    ├── generate_animated_episode.py   # Multi-layer video compositor (Ken Burns + SFX + ASS)
    ├── upload_to_youtube.py          # Zero-dependency YouTube uploader & playlist router
    ├── autonomous_100_days_scheduler.py # 100-Day automated 2x daily cloud scheduler
    ├── generate_episode_assets.py     # Batch folder & asset directory builder
    └── assemble_episode_video.py      # Audio melody generator & scene previewer
```

---

## 🔒 Security Notice
This repository is 100% credential-free. Never commit your private `client_secrets.json` or `token.json` files. They are automatically ignored via `.gitignore`.

---

## 📄 License
MIT License. Created for the AI Automation & Content Creator Community.
