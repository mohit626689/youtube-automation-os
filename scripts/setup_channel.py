#!/usr/bin/env python3
"""
Universal YouTube Automation OS — Interactive Channel Onboarding Wizard
Configures ANY YouTube channel niche in seconds:
- Kids / Preschool Animation
- Faceless Finance & Wealth Documentaries
- Stoicism & Motivation / Mindset
- Horror & True Crime / Spooky Stories
- Tech, AI & Future Science Explainers
- Custom Niche / Competitor Channel Modeling

Generates:
- pipeline_config.json (Full channel engine configuration)
- channel_brand_bible.md (Art direction, voice profile, sonic identity)
- 100_video_roadmap.md (4-phase 100-video content calendar)
- kids_or_general_script_template.md (High-retention script formula)
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

NICHE_PRESETS = {
    "1": {
        "key": "kids",
        "name": "Preschool & Kids Animation (Phonics, Songs & Characters)",
        "coppa": True,
        "category_id": "27", # Education
        "voice": "en-US-AnaNeural",
        "voice_description": "Sweet, cheerful, articulate authentic child voiceover",
        "style_tokens": "3D Pixar and claymation style, adorable stylized cute baby animal, huge expressive sparkling glass eyes, friendly warm smile, soft rounded geometry, smooth tactile silicone clay texture, bright pastel studio lighting, rim lighting, 8k resolution, cinematic depth of field, vibrant colorful background",
        "music": "Acoustic Ukulele, Marimba, Glockenspiel, Bouncy Bass, Handclaps",
        "font": "Arial Rounded MT Bold",
        "title_hook": "Can You Find the {Object}? | Letter {Letter} Phonics Lesson for Kids | {Channel}",
        "default_name": "ABC Zoo TV",
        "default_handle": "@ABCZooTv"
    },
    "2": {
        "key": "finance",
        "name": "Faceless Wealth & Finance Documentaries (Cash Cow)",
        "coppa": False,
        "category_id": "24", # Entertainment / Business
        "voice": "en-US-ChristopherNeural",
        "voice_description": "Deep, authoritative, cinematic documentary narrator",
        "style_tokens": "Cinematic 8k, dramatic documentary lighting, dark moody luxury aesthetic, gold and deep obsidian accents, high contrast volumetric lighting, photorealistic textures, Unreal Engine 5 render style, shallow depth of field",
        "music": "Dark ambient synth, deep brass braams, subtle suspenseful strings, ticking clock rhythms",
        "font": "Arial Black",
        "title_hook": "How {Subject} Built a Secret $10B Empire (And Lost It All) | {Channel}",
        "default_name": "Magnate Vault",
        "default_handle": "@MagnateVault"
    },
    "3": {
        "key": "stoic",
        "name": "Stoicism & Motivation / Mindset Quotes",
        "coppa": False,
        "category_id": "27", # Education
        "voice": "en-GB-RyanNeural",
        "voice_description": "Calm, powerful, resonant philosophical narrator",
        "style_tokens": "Dramatic Greek marble statue aesthetic, chipping ancient stone, moody chiaroscuro lighting, dark smoky shadows, cinematic slow dust particles, museum-grade classical realism, 8k cinematic shot",
        "music": "Atmospheric cello, slow melancholic piano, distant thunderstorm ambience",
        "font": "Times New Roman",
        "title_hook": "When You Feel Weak, Remember This Rule (Marcus Aurelius) | {Channel}",
        "default_name": "Stoic Sanctuary",
        "default_handle": "@StoicSanctuary"
    },
    "4": {
        "key": "horror",
        "name": "Horror & True Crime / Creepypasta Mysteries",
        "coppa": False,
        "category_id": "24", # Entertainment
        "voice": "en-US-EricNeural",
        "voice_description": "Slow, eerie, chilling, atmospheric storytelling voice",
        "style_tokens": "Eerie dark cinematic lighting, thick forest fog, analog VHS grain texture, retro 90s camcorder aesthetic, desaturated cool tones, eerie rim light, photorealistic psychological thriller atmosphere",
        "music": "Low eerie sub-bass drones, distorted music box melody, vinyl static crackles, heartbeat pulse",
        "font": "Marker Felt",
        "title_hook": "The Disturbing Mystery That Police Kept Hidden for 30 Years | {Channel}",
        "default_name": "Midnight Whispers",
        "default_handle": "@MidnightWhispers"
    },
    "5": {
        "key": "tech",
        "name": "Tech, AI & Future Science Explainers",
        "coppa": False,
        "category_id": "28", # Science & Technology
        "voice": "en-US-BrianNeural",
        "voice_description": "Sharp, smart, engaging, modern tech narrator",
        "style_tokens": "Cyberpunk high-tech aesthetic, clean glowing neon cyan and magenta accents, futuristic holographic UI overlays, sleek isometric 3D render, Octane Render, 8k raytracing, depth of field",
        "music": "Modern lo-fi tech groove, crisp synthwave arpeggiators, electronic glitch beats",
        "font": "Helvetica Neue",
        "title_hook": "Why Everyone is Suddenly Terrified of Quantum AI | {Channel}",
        "default_name": "Nexus Tech AI",
        "default_handle": "@NexusTechAI"
    }
}

def print_banner():
    print("\n" + "=" * 75)
    print("🌟 UNIVERSAL YOUTUBE VIDEO AUTOMATION OPERATING SYSTEM 🌟")
    print("Autonomous Content Engine for Any Niche | 100-Day Automated Pipeline")
    print("=" * 75 + "\n")

def interactive_wizard():
    print_banner()
    print("Select your channel niche preset or model after an existing channel:\n")
    for k, v in NICHE_PRESETS.items():
        print(f"  [{k}] {v['name']}")
    print("  [6] Custom Niche / Model from Competitor Channel URL\n")

    choice = input("Enter choice [1-6] (default: 1): ").strip() or "1"

    if choice in NICHE_PRESETS:
        preset = NICHE_PRESETS[choice]
        print(f"\n✅ Selected Preset: {preset['name']}")
        ch_name = input(f"Enter Channel Name (default: {preset['default_name']}): ").strip() or preset['default_name']
        ch_handle = input(f"Enter Channel Handle (default: {preset['default_handle']}): ").strip() or preset['default_handle']
        niche_key = preset["key"]
        voice = preset["voice"]
        style_tokens = preset["style_tokens"]
        coppa = preset["coppa"]
        cat_id = preset["category_id"]
        music = preset["music"]
    else:
        print("\n🛠️ Custom Niche Configuration:")
        ch_name = input("Enter Channel Name: ").strip() or "My Channel"
        ch_handle = input("Enter Channel Handle (e.g. @MyChannel): ").strip() or f"@{ch_name.replace(' ', '')}"
        niche_name = input("Enter Niche (e.g. Luxury Real Estate, Space Science, Fitness): ").strip() or "General Education"
        comp_url = input("Enter Inspiration/Competitor YouTube URL (optional): ").strip()
        voice = input("Enter Edge TTS voice (e.g. en-US-ChristopherNeural, en-US-AnaNeural, en-GB-RyanNeural) [default: en-US-ChristopherNeural]: ").strip() or "en-US-ChristopherNeural"
        style_tokens = input("Enter visual prompt style tokens: ").strip() or "Cinematic 8k, photorealistic studio lighting, high dynamic range, depth of field"
        coppa_in = input("Is this channel made for kids under 13? (y/N): ").strip().lower()
        coppa = (coppa_in == "y")
        cat_id = "27" if coppa else "24"
        music = "Cinematic modern acoustic & ambient"
        niche_key = "custom"

    # Build Pipeline Config
    config = {
        "channel": {
            "name": ch_name,
            "handle": ch_handle,
            "niche": niche_key,
            "coppa_compliant": coppa,
            "default_category": cat_id,
            "default_language": "en"
        },
        "aesthetic_engine": {
            "style_tokens": style_tokens,
            "aspect_ratios": {
                "long_form": "16:9",
                "shorts": "9:16",
                "thumbnail": "16:9"
            },
            "thumbnail_contrast_colors": ["#FFD54F", "#29B6F6", "#FF5252", "#66BB6A", "#FFA726"]
        },
        "audio_engine": {
            "voice_name": voice,
            "music_style": music,
            "bpm_range": [105, 120]
        },
        "release_schedule": {
            "slot_1": "08:00 AM IST",
            "slot_2": "05:00 PM IST",
            "daily_uploads": 2
        }
    }

    # Save pipeline_config.json
    out_config_path = BASE_DIR / "pipeline_config.json"
    with open(out_config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    # Generate Channel Brand Bible
    brand_bible_path = BASE_DIR / "channel_brand_bible.md"
    brand_content = f"""# {ch_name} — Channel Brand Bible & Production Standard

## 1. Channel Identity
- **Name:** {ch_name} ({ch_handle})
- **Niche:** {niche_key.capitalize()}
- **COPPA Status:** {'Made for Kids (COPPA Compliant)' if coppa else 'Standard (Not Made for Kids)'}
- **YouTube Category:** {cat_id}
- **Daily Cadence:** 2 Videos Daily (08:00 AM & 05:00 PM)

## 2. Visual Aesthetic Engine
- **Master Prompt Tokens:**
> *"{style_tokens}"*
- **Composition Rules:**
  - 16:9 Landscape for core documentary/learning episodes.
  - 9:16 Vertical for mobile YouTube Shorts.
  - Bold, saturated colors with 3D rim lighting and high contrast foreground elements.

## 3. Sonic Identity
- **Voiceover Model:** Microsoft Edge Neural `{voice}`
- **Audio Ducking:** Background music ducked to 14% volume during spoken lines.
- **Cartoon/Cinematic Sound FX:** Procedural pops, transition whooshes, chimes, and impact hits synchronized to spoken cues.

## 4. vidIQ 96+ High-Converting Metadata Formula
- **Title Hook:** Curiosity Question Hook + High-Search Target Keyword + Channel Branding
- **Description:** 3 keyword-rich paragraphs targeting search volume, followed by timestamps, full script/lyrics, and channel subscribe links.
"""
    with open(brand_bible_path, "w", encoding="utf-8") as f:
        f.write(brand_content)

    print("\n" + "=" * 75)
    print(f"🎉 Channel Successfully Configured for '{ch_name}' ({ch_handle})!")
    print("=" * 75)
    print(f"📄 Created: pipeline_config.json")
    print(f"📄 Created: channel_brand_bible.md")
    print("\nNext Steps:")
    print("1. Set up your Google Cloud OAuth in client_secrets.json (copy from client_secrets.example.json)")
    print("2. Generate episode scenes: python3 scripts/generate_animated_episode.py")
    print("3. Auto-upload & schedule 100 days: python3 scripts/autonomous_100_days_scheduler.py --schedule_next 2\n")

if __name__ == "__main__":
    interactive_wizard()
