---
name: youtube-automation
description: Universal autonomous YouTube channel automation operating system for ANY niche (Kids, Faceless Finance & Wealth, Stoic Motivation, True Crime/Horror, Tech & AI, or Custom). Powered exclusively by HyperFrames (heygen-com/hyperframes) for 60fps butter-smooth HTML/CSS/GSAP video composition, 400+ neural voices (Edge TTS), synchronized SFX, kinetic subtitle streams, vidIQ 96-score SEO metadata, and 100-day autonomous scheduled publishing (8 AM & 5 PM daily) via YouTube Data API v3.
compatibility: Python 3.10+, FFmpeg with libass, Node.js 18+, HyperFrames 0.8+, YouTube Data API v3
metadata:
  standard: "agentskills.io"
  version: "2.1.0"
  author: "Antigravity OS"
---

# Universal YouTube Automation Operating System (HyperFrames Edition)

A broadcast-grade, end-to-end autonomous operating system designed to run **any YouTube channel niche** completely hands-free for 100+ days, utilizing **HyperFrames** as the exclusive 60fps video rendering and editing engine.

---

## ⚡ Triggers & Activation

Activate this skill when:
- The user wants to start, automate, produce, or scale ANY YouTube channel (Kids, Faceless Finance, Stoicism, Horror, Tech, Documentary, or Custom).
- The user wants to model or clone an existing YouTube channel's format, tone, and visual style.
- The user requests scripts, visual scene prompts, or character IP generation.
- The user asks to compose, render, or edit videos in 1080p Landscape (16:9) or Shorts (9:16) using **HyperFrames**.
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
    ├── render_hyperframes_episode.py  # Primary 60fps HyperFrames compositor (HTML/CSS/GSAP)
    ├── generate_animated_episode.py   # Multi-layer video compositor (HyperFrames default)
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

### 3. HyperFrames 60fps Video Composition & Editing (Exclusive Engine)
HyperFrames (`heygen-com/hyperframes`) is the sole video compositor and editor across all formats:

```bash
# Render both 16:9 Landscape and 9:16 Shorts via HyperFrames
python3 scripts/render_hyperframes_episode.py --episode_dir "episodes/Ep_001" --format both

# Or execute master animated pipeline (defaults to HyperFrames):
python3 scripts/generate_animated_episode.py --episode_dir "episodes/Ep_001" --format both --engine hyperframes
```

#### HyperFrames Key Capabilities:
- **60fps Butter-Smooth Easing:** GSAP `power1.inOut` camera pans and `back.out(2)` pop-in entrances.
- **Triple-Tier Shorts Layout (9:16):** Full 1080x1920 ambient blurred background + 1040x585 crisp cinema stage card with white stroke & drop shadow + gold header + kinetic rounded pill subtitles.
- **Cinematic Landscape (16:9):** Seamless 1920x1080 canvas, floating mascot badge with 2.8s sinusoidal hover physics, and interactive spotlight pointer.
- **Direct CLI Validation & Rendering:**
  ```bash
  # Validate composition syntax
  npx hyperframes check episodes/Ep_001/hyperframes/composition_shorts.html

  # Render master MP4 (non-interactive, 60fps)
  npx hyperframes render episodes/Ep_001/hyperframes/composition_shorts.html -o episodes/Ep_001/final_animated_shorts.mp4 --fps 60 --quality looks --non-interactive
  ```

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
