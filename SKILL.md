---
name: youtube-automation
description: Universal autonomous YouTube channel automation operating system for ANY niche (Kids, Faceless Finance & Wealth, Stoic Motivation, True Crime/Horror, Tech & AI, or Custom). Features interactive channel onboarding (setup.py) to clone/model any channel, 400+ neural voices (Edge TTS), dynamic zero-overlap video composition with synchronized SFX, rotating ASS subtitles, vidIQ 96-score SEO metadata, and 100-day autonomous scheduled publishing (8 AM & 5 PM daily) via YouTube Data API v3.
compatibility: Python 3.10+, FFmpeg with libass, Node.js 18+, YouTube Data API v3
metadata:
  standard: "agentskills.io"
  version: "2.0.0"
  author: "Antigravity OS"
---

# Universal YouTube Automation Operating System

A broadcast-grade, end-to-end autonomous operating system designed to run **any YouTube channel niche** completely hands-free for 100+ days.

---

## ⚡ Triggers & Activation

Activate this skill when:
- The user wants to start, automate, produce, or scale ANY YouTube channel (Kids, Faceless Finance, Stoicism, Horror, Tech, Documentary, or Custom).
- The user wants to model or clone an existing YouTube channel's format, tone, and visual style.
- The user requests scripts, visual scene prompts, or character IP generation.
- The user asks to compose, render, or animate videos in 1080p Landscape (16:9) or Shorts (9:16).
- The user needs authentic neural voiceover (from 400+ Edge TTS models across languages and age groups).
- The user wants auto-uploading and 100-day cloud scheduling on YouTube with vidIQ 96+ SEO metadata.

---

## 🏛️ System Architecture

```
youtube-automation/
├── setup.py                          # 1-Click Interactive Onboarding Wizard
├── pipeline_config.json              # Master channel configuration, voice, colors & schedule
├── channel_brand_bible.md            # Visual style tokens, sonic identity, and prompt standards
├── 100_video_roadmap.md              # 4-Phase sequential 100-video content calendar
├── kids_or_general_script_template.md# 5-Scene high-retention script formula
└── scripts/
    ├── setup_channel.py              # Interactive niche & competitor channel analyzer
    ├── generate_neural_child_voice.js # Neural voice synthesis engine (Edge TTS 400+ voices)
    ├── generate_animated_episode.py   # Multi-layer video compositor (Ken Burns + SFX + zero-overlap ASS)
    ├── upload_to_youtube.py          # Zero-dependency YouTube uploader & playlist router
    └── autonomous_100_days_scheduler.py # 100-Day 2x daily (8 AM & 5 PM) cloud scheduler
```

---

## 🚀 Supported Niche Presets

The onboarding wizard (`python3 setup.py`) includes plug-and-play engines for:
1. **Preschool & Toddler Animation** (3D Clay-Pixar style, child voice `en-US-AnaNeural`, COPPA certified)
2. **Faceless Wealth & Finance Documentaries** (Cinematic 8K luxury dark aesthetic, deep narrator `en-US-ChristopherNeural`)
3. **Stoic & Motivational Mindset** (Greco-Roman marble statue aesthetic, powerful voice `en-GB-RyanNeural`)
4. **Horror & True Crime Mysteries** (Eerie analog VHS grain aesthetic, slow chilling narrator `en-US-EricNeural`)
5. **Tech, AI & Future Science Explainers** (Cyberpunk neon & holographic aesthetic, sharp tech voice `en-US-BrianNeural`)
6. **Custom Niche / Model from Competitor URL** (Analyzes any competitor channel and generates a tailored pipeline)

---

## 🛠️ Core Commands & Execution

### 1. Interactive Onboarding & Channel Setup
```bash
python3 setup.py
# Or: npm run setup
```
Asks for niche, competitor channel URL, visual aesthetic, and voice preference, then automatically builds `pipeline_config.json` and `channel_brand_bible.md`.

### 2. Neural Voiceover Synthesis
```bash
node scripts/generate_neural_child_voice.js "episodes/Ep_001" "en-US-ChristopherNeural"
```

### 3. Dynamic Sequential Video Assembly
```bash
python3 scripts/generate_animated_episode.py --episode_dir "episodes/Ep_001" --format both --theme 0
```
- **Zero Voice Overlaps:** Dynamically measures speech durations with `ffprobe` and chains audio sequentially with natural breathing gaps.
- **Zero Subtitle Collisions:** Clamps ASS subtitle display to clear the screen before the next dialogue appears.
- **Synchronized SFX:** Audio cues (chimes, impacts, whooshes) automatically anchor to spoken words.

### 4. vidIQ Score 96+ Upload & Automatic Playlist Sorting
```bash
python3 scripts/upload_to_youtube.py \
  --episode_dir "episodes/Ep_001" \
  --format landscape \
  --privacy unlisted
```
Applies high-CTR curiosity question titles, 3-paragraph keyword descriptions, and routes to target playlists.

### 5. 100-Day Autonomous Scheduling (8 AM & 5 PM Daily)
```bash
python3 scripts/autonomous_100_days_scheduler.py --schedule_next 2
```
Schedules videos directly on YouTube using `publishAt`. YouTube flips them to Public automatically at 08:00 AM and 05:00 PM without requiring your computer to stay on.
