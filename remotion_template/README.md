# ABC Zoo TV — Remotion Video Composition Template

This template provides a React-based programmatic video rendering pipeline for **ABC Zoo TV**.

---

## 1. Quick Start

### Installation
```bash
npm install
```

### Live Preview Mode
Launches the browser-based Remotion Player with hot-reloading:
```bash
npm start
```

### Render Full Video
To render 16:9 Landscape YouTube episode:
```bash
npm run build:landscape
```

To render 9:16 Vertical YouTube Shorts:
```bash
npm run build:shorts
```

---

## 2. Fast Alternative: Native FFmpeg Assembler

For zero-dependency rendering directly from your terminal in seconds, use our Python FFmpeg compositor:
```bash
python3 scripts/assemble_episode_video.py --episode_dir episodes/Ep_001_Letter_A --format both
```
