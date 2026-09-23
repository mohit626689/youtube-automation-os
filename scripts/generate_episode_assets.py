#!/usr/bin/env python3
"""
ABC Zoo TV — Automated Episode Asset & Packaging Engine
Generates complete production packages for each episode:
  - 5-Scene High-Retention Kids Script & Rhyme Lyrics
  - Scene-by-Scene Visual Prompts (3D Clay/Pixar Aesthetic)
  - High-CTR Thumbnail Prompt & Color Hierarchy
  - YouTube COPPA-Compliant SEO Metadata (Title, Description, Tags, Chapters)
  - Synced Subtitle SRT Template
"""

import os
import json
import argparse
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "pipeline_config.json"
OUTPUT_DIR = BASE_DIR / "episodes"

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file missing at {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_script(char_info, letter, next_char_info, next_letter):
    name = char_info["name"]
    animal = char_info["animal"]
    color = char_info["color"]
    sound = char_info["phonics_sound"]
    objs = char_info["primary_objects"]
    obj1 = objs[0]
    obj2 = objs[1] if len(objs) > 1 else "Toy"
    obj3 = objs[2] if len(objs) > 2 else "Friend"
    
    script_md = f"""# Episode Script: Letter {letter} Song — {name} the {animal} & The {obj1} Adventure
**Channel:** ABC Zoo TV (@ABCZooTv)
**Target Demographic:** Toddlers & Preschoolers (Ages 1–5)
**Duration:** ~2 minutes 20 seconds
**BPM:** 112 BPM (Acoustic Ukulele, Marimba, Bouncy Bass, Handclaps)
**Lead Mascot:** {name} the {animal} (Signature Color: {color})

---

### [0:00 - 0:08] SCENE 1: THE SENSORY HOOK & GREETING
* **Visual:** Camera rapid zoom into bright sunny jungle meadow. {name} the {animal} pops out from behind a giant shiny 3D {obj1} with a silly wiggle, waving both hands with oversized sparkling eyes.
* **Audio SFX:** Playful ascending xylophone slide + bright cartoon *BOING*!
* **Spoken Intro (Enthusiastic & Clear):**
  "{name}: Hi friends! I'm {name} the {animal}! Look what I found... It's the Letter {letter}!
  Can you say {letter} with me? {sound} {sound} {obj1}!"

---

### [0:08 - 0:38] SCENE 2: VERSE 1 — THE PHONICS RHYME
* **Music:** Bouncy acoustic ukulele and clapping beat starts (112 BPM).
* **Visual:** {name} hops happily across colorful numbered stepping stones. Giant 3D {obj1} drops down with a soft jelly bounce and sparkly stars.
* **Song Lyrics (AABB Rhyme Scheme):**
  "{letter} is for {name}, playing every day,
  {letter} is for {obj1}, hip hip hooray!
  {sound} {sound} {obj1}, crunchy and sweet,
  Singing Letter {letter} is a happy little treat!"
* **Visual Transition (0:24):** Camera pans left, floating bubbles reveal a shiny {obj2}!

---

### [0:38 - 1:10] SCENE 3: HIGH-ENERGY CHORUS (PHYSICAL DANCE MOVEMENT)
* **Music:** Marimba swells with lively brass beats.
* **Visual:** Yellow bouncing star highlights uppercase '{letter}' and lowercase '{letter.lower()}' on screen. {name} does a signature wiggle-tail dance.
* **Song Lyrics:**
  "{letter}, {letter}, {letter}! Let's jump up high!
  Reach for the {obj1} in the sunny sky!
  Wiggle your toes and clap with cheer,
  The happy Letter {letter} is finally here!"
* **Interactive Graphic:** Big glowing letters flash: "CAN YOU JUMP?" with cheerful toddler giggles.

---

### [1:10 - 1:45] SCENE 4: INTERACTIVE GAME — "SPOT THE '{letter}' OBJECT"
* **Music:** Drops to gentle rhythmic marimba tick-tock thinking groove.
* **Visual:** Three colorful floating bubbles appear on screen:
  - Bubble 1: A giant shiny {obj1}
  - Bubble 2: A silly blue Shoe (Distractor 1)
  - Bubble 3: A yellow Banana (Distractor 2)
* **Spoken Interaction:**
  "{name}: Let's play a game! Which one starts with {sound}?
  Is it the Shoe, the {obj1}, or the Banana?
  Can you point to the {sound} {obj1}?"
  *(1.5-second pause with thinking chimes)*
  *SFX: Joyful chime ding!*
  "{name}: That's right! You found the {obj1}! You're so smart! High five!"

---

### [1:45 - 2:10] SCENE 5: VERSE 2 & FINALE CELEBRATION
* **Music:** Full celebratory ensemble with tambourines and happy handclaps.
* **Visual:** Confetti, gentle floating stars, and {name} playing with {obj3}.
* **Song Lyrics:**
  "{letter} is for {obj3}, shining bright and bold,
  The greatest little letter that was ever told!
  {letter}, {letter}, {letter}, sing it loud and proud,
  Sing with {name} to the whole zoo crowd!"

---

### [2:10 - 2:25] SCENE 6: NEXT-EPISODE SEAMLESS HANDOFF
* **Visual:** {next_char_info['name']} the {next_char_info['animal']} peeks from behind a cozy tree holding Letter {next_letter}.
* **Spoken Outro:**
  "{name}: Yay! You learned Letter {letter}!
  Look who wants to play next... It's my best friend {next_char_info['name']}!
  Click right here to meet {next_char_info['name']} and learn Letter {next_letter}!"
* **End Screen Overlay:** Autoplay card linking directly to Letter {next_letter} Episode + Full ABC Zoo Playlist.
"""
    return script_md

def generate_visual_prompts(char_info, letter, config):
    style = config["aesthetic_engine"]["style_tokens"]
    name = char_info["name"]
    animal = char_info["animal"]
    color = char_info["color"]
    objs = char_info["primary_objects"]
    
    prompts = [
        {
            "scene": 1,
            "timestamp": "0:00 - 0:08",
            "shot_type": "Extreme Close-Up to Medium Zoom",
            "prompt": f"{style}, friendly cute baby {animal.lower()} named {name} with soft {color.lower()} skin, huge smiling expressive glass eyes, waving happily, popping out from behind a giant glossy 3D letter '{letter}' and a giant red {objs[0].lower()}, bright sunny pastel jungle background, soft volumetric rim lighting --ar 16:9"
        },
        {
            "scene": 2,
            "timestamp": "0:08 - 0:38",
            "shot_type": "Wide Action Shot",
            "prompt": f"{style}, cute baby {animal.lower()} hopping across colorful stepping stones in a whimsical candy-colored meadow, oversized floating 3D {objs[0].lower()} with magical sparkles, floating bubbles with miniature {objs[1].lower()}, vibrant saturated colors --ar 16:9"
        },
        {
            "scene": 3,
            "timestamp": "0:38 - 1:10",
            "shot_type": "Dynamic Dance Mid-Shot",
            "prompt": f"{style}, adorable baby {animal.lower()} dancing and jumping joyfully with arms in the air, big glowing golden uppercase letter '{letter}' and lowercase '{letter.lower()}' floating overhead with gentle sunburst halo, whimsical flowers, joyful expression --ar 16:9"
        },
        {
            "scene": 4,
            "timestamp": "1:10 - 1:45",
            "shot_type": "Interactive Game Setup",
            "prompt": f"{style}, baby {animal.lower()} pointing excitedly to the right where three colorful translucent bubbles float: inside one bubble is a vibrant {objs[0].lower()}, in another a cartoon shoe, in another a yellow banana, clean bright sky blue backdrop --ar 16:9"
        },
        {
            "scene": 5,
            "timestamp": "1:45 - 2:10",
            "shot_type": "Celebration Wide Shot",
            "prompt": f"{style}, baby {animal.lower()} celebrating with colorful paper confetti falling, holding a mini {objs[2].lower()}, joyful open-mouth laugh, surrounded by warm rainbow hues and glowing stars --ar 16:9"
        },
        {
            "scene": 6,
            "timestamp": "2:10 - 2:25",
            "shot_type": "Two-Character Handoff Shot",
            "prompt": f"{style}, baby {animal.lower()} on the left smiling and pointing to a friendly cute baby animal on the right peeking around a pastel tree trunk holding a colorful letter, end card composition, clean uncluttered layout --ar 16:9"
        }
    ]
    return prompts

def generate_thumbnail_prompt(char_info, letter, config):
    style = config["aesthetic_engine"]["style_tokens"]
    name = char_info["name"]
    animal = char_info["animal"]
    color = char_info["color"]
    obj1 = char_info["primary_objects"][0]
    
    prompt = (
        f"{style}, extreme close-up portrait of cute baby {animal.lower()} with enormous sparkling eyes and an ecstatic joyful smile, "
        f"holding a glossy giant vibrant red {obj1.lower()} and a glowing golden 3D letter '{letter}', "
        f"vibrant saturated high-contrast cyan sky background, studio rim lighting on {color.lower()} fur, "
        f"hyper-clean visual hierarchy, high click-through rate preschool thumbnail composition --ar 16:9 --stylize 250"
    )
    
    spec = {
        "text_overlay": f"LETTER {letter}!",
        "font_specs": "Extra-bold rounded bubble font, Pure White #FFFFFF with 8px Midnight Blue #1A237E border & soft drop shadow",
        "focal_points": [
            f"1. Baby {animal}'s expressive eyes (top center-left)",
            f"2. Giant glowing Letter '{letter}' (top right)",
            f"3. Glossy vibrant {obj1} (bottom center-right)"
        ],
        "color_contrast_breakdown": {
            "background": "Vibrant Cyan Sky (#29B6F6)",
            "character": f"{color} ({char_info['hex']})",
            "accent_prop": "Crimson Red & Golden Yellow (#FFD54F)"
        },
        "raw_image_prompt": prompt
    }
    return spec

def generate_metadata(char_info, letter, next_char_info, next_letter):
    name = char_info["name"]
    animal = char_info["animal"]
    obj1 = char_info["primary_objects"][0]
    obj2 = char_info["primary_objects"][1]
    sound = char_info["phonics_sound"]
    
    title = f"Letter {letter} Song | {name} the {animal} & {obj1} | ABC Phonics Nursery Rhymes for Kids"
    description = f"""Welcome to ABC Zoo TV! Sing along with {name} the {animal} to learn the Letter {letter} and its sound {sound}! 

Join {name} on an exciting preschool adventure exploring {obj1.lower()}s, {obj2.lower()}s, and fun phonics games! 

🎨 Sing, dance, and learn phonics with the ABC Zoo Pals every week!
👉 Subscribe for more preschool songs: https://www.youtube.com/@ABCZooTv?sub_confirmation=1

⏰ TIMESTAMPS:
0:00 - Meet {name} the {animal} & Letter {letter}!
0:08 - Letter {letter} Phonics Song ({obj1})
0:38 - Jump & Dance Chorus!
1:10 - Can You Spot the {obj1}? (Interactive Game)
1:45 - Letter {letter} Celebration!
2:10 - Next Up: Letter {next_letter} with {next_char_info['name']}!

#ABCZooTV #Letter{letter} #PhonicsSong #PreschoolLearning #KidsSongs #NurseryRhymes #LearnAlphabet #ToddlerSongs
"""
    tags = [
        f"letter {letter.lower()} song",
        f"letter {letter.lower()} phonics",
        f"phonics letter {letter.lower()}",
        f"{name.lower()} the {animal.lower()}",
        "abc zoo tv",
        "abc phonics song",
        "alphabet songs for kids",
        "nursery rhymes",
        "toddler learning videos",
        "preschool alphabet",
        "learn letter sounds",
        "educational kids cartoons",
        "songs for toddlers",
        "kindergarten phonics"
    ]
    
    return {
        "title": title,
        "description": description.strip(),
        "tags": tags,
        "made_for_kids": True,
        "category_id": "27",
        "default_language": "en"
    }

def generate_srt(char_info, letter, next_char_info, next_letter):
    name = char_info["name"]
    animal = char_info["animal"]
    sound = char_info["phonics_sound"]
    obj1 = char_info["primary_objects"][0]
    obj2 = char_info["primary_objects"][1]
    
    srt_content = f"""1
00:00:00,500 --> 00:00:03,800
Hi friends! I'm {name} the {animal}!

2
00:00:04,000 --> 00:00:07,500
Look what I found... It's the Letter {letter}!

3
00:00:07,800 --> 00:00:11,500
Can you say {letter} with me? {sound} {sound} {obj1}!

4
00:00:12,000 --> 00:00:15,800
{letter} is for {name}, playing every day!

5
00:00:16,000 --> 00:00:19,800
{letter} is for {obj1}, hip hip hooray!

6
00:00:20,000 --> 00:00:24,200
{sound} {sound} {obj1}, crunchy and sweet!

7
00:00:24,500 --> 00:00:29,000
Singing Letter {letter} is a happy little treat!

8
00:00:38,000 --> 00:00:41,500
{letter}, {letter}, {letter}! Let's jump up high!

9
00:00:41,800 --> 00:00:45,500
Reach for the {obj1} in the sunny sky!

10
00:00:46,000 --> 00:00:49,500
Wiggle your toes and clap with cheer!

11
00:00:49,800 --> 00:00:54,000
The happy Letter {letter} is finally here!

12
00:01:10,000 --> 00:01:14,000
Let's play a game! Which one starts with {sound}?

13
00:01:14,500 --> 00:01:18,500
Can you point to the {sound} {obj1}?

14
00:01:21,000 --> 00:01:24,500
That's right! You found the {obj1}! Good job!

15
00:01:45,000 --> 00:01:49,000
{letter} is for {obj2}, shining bright and bold!

16
00:01:49,500 --> 00:01:54,000
The greatest little letter that was ever told!

17
00:02:10,000 --> 00:02:14,500
Look who wants to play next... It's my best friend {next_char_info['name']}!

18
00:02:15,000 --> 00:02:19,500
Click right here to meet {next_char_info['name']} and learn Letter {next_letter}!
"""
    return srt_content.strip()

def build_episode_package(letter, config):
    characters = config["characters"]
    letter = letter.upper()
    if letter not in characters:
        raise ValueError(f"Letter '{letter}' not found in pipeline characters.")
    
    # Determine next character
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    idx = alphabet.index(letter)
    next_letter = alphabet[(idx + 1) % len(alphabet)]
    
    char_info = characters[letter]
    next_char_info = characters[next_letter]
    
    ep_num = str(idx + 1).zfill(3)
    ep_dir = OUTPUT_DIR / f"Ep_{ep_num}_Letter_{letter}"
    ep_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Script
    script_content = generate_script(char_info, letter, next_char_info, next_letter)
    with open(ep_dir / f"script_letter_{letter.lower()}.md", "w", encoding="utf-8") as f:
        f.write(script_content)
        
    # 2. Visual Prompts
    prompts = generate_visual_prompts(char_info, letter, config)
    with open(ep_dir / f"visual_prompts_letter_{letter.lower()}.json", "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2)
        
    # 3. Thumbnail Spec
    thumb = generate_thumbnail_prompt(char_info, letter, config)
    with open(ep_dir / f"thumbnail_spec_letter_{letter.lower()}.json", "w", encoding="utf-8") as f:
        json.dump(thumb, f, indent=2)
        
    # 4. YouTube SEO Metadata
    meta = generate_metadata(char_info, letter, next_char_info, next_letter)
    with open(ep_dir / f"metadata_letter_{letter.lower()}.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        
    # 5. Synced Subtitles SRT
    srt = generate_srt(char_info, letter, next_char_info, next_letter)
    with open(ep_dir / f"subtitles_letter_{letter.lower()}.srt", "w", encoding="utf-8") as f:
        f.write(srt)
        
    print(f"✅ Successfully built complete production package for Episode {ep_num} (Letter {letter}) at: {ep_dir}")
    return ep_dir

def main():
    parser = argparse.ArgumentParser(description="ABC Zoo TV Episode Asset Generator")
    parser.add_argument("--letter", type=str, default="A", help="Alphabet letter to generate (A-Z) or 'ALL'")
    args = parser.parse_args()
    
    config = load_config()
    
    if args.letter.upper() == "ALL":
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            build_episode_package(char, config)
        print("🎉 All 26 Phonics Episode Packages Generated Successfully!")
    else:
        build_episode_package(args.letter, config)

if __name__ == "__main__":
    main()
