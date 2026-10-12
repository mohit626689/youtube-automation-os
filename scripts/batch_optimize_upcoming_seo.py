#!/usr/bin/env python3
"""
Batch Video SEO & Thumbnail Optimizer
Renders native 16:9 thumbnails and applies high-score vidIQ metadata to upcoming videos.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))
from update_youtube_video_seo import update_video_seo

EPISODES_TO_OPTIMIZE = [
    {
        "video_id": "IhNZ2oid2Jk", # Day 28 (Brush Teeth)
        "ep_dir": BASE_DIR / "episodes/Ep_028_Brush_Teeth",
        "title": "Brush Your Teeth Song for Kids! 🪥 2-Minute Morning & Bedtime Routine | ABC Zoo TV",
        "badge": "BRUSH TEETH!",
        "sticker": "🪥 2-MIN ROUTINE",
        "ribbon": "SPARKLE SMILE",
        "description": """Sing, brush, and smile with the 2-minute Brush Your Teeth Song! 🪥 Join Barnaby Bear and Coco Cat for a healthy hygiene adventure in ABC Zoo.

Watch Barnaby and Coco show little ones how fun brushing teeth can be in this colorful kids animation. Follow along as they brush round and round, up and down, making it easy for toddlers and preschoolers to build healthy daily habits in a bright, friendly environment.

This interactive nursery rhyme is designed for preschool learning, helping children establish positive morning and bedtime routines. Use this video as a fun 2-minute timer to help your child brush their teeth every day.

🔔 Subscribe to ABC Zoo TV for more healthy routine songs and toddler songs:
https://www.youtube.com/@ABCZooTv?sub_confirmation=1

⭐ Song Lyrics:
Hi friends! Barnaby and Coco are ready to brush our teeth!
Grab your toothbrush and let us make our smiles sparkle!
Brush, brush, brush your teeth, round and round and clean!
Up and down and all around, the brightest smile you've seen!
Swish, spit, rinse it out, hip hip hooray!
Can you show me your big shiny smile? Say cheese!
Super sparkle! Clean teeth every morning and night!
See you tomorrow for morning wake up! Bye-bye!

TIMESTAMPS:
0:00 - Meet Barnaby Bear & Coco Cat
0:05 - Grab Your Toothbrush!
0:15 - Brush Round and Round
0:28 - Interactive "Say Cheese" Smile Game
0:40 - Super Sparkle Celebration

#ABCZooTV #BrushYourTeethSong #KidsAnimation #PreschoolLearning #HealthyHabits #ToddlerSongs #NurseryRhymes #TeethBrushing
""",
        "tags": [
            "Brush Your Teeth Song for Kids", "brush teeth song", "2 minute brush teeth",
            "toddler brush teeth song", "preschool learning", "healthy habits for kids",
            "kids animation", "toddler songs", "ABC Zoo TV", "bedtime routine for toddlers",
            "morning routine for kids", "nursery rhymes"
        ]
    },
    {
        "video_id": "KLRiplXxqiQ", # Day 29 (Good Morning)
        "ep_dir": BASE_DIR / "episodes/Ep_029_Morning_Wakeup",
        "title": "Good Morning Wake Up Song for Kids! ☀️ Happy Sunrise Routine | ABC Zoo TV",
        "badge": "WAKE UP!",
        "sticker": "☀️ MORNING SONG",
        "ribbon": "HAPPY SUNRISE",
        "description": """Start the day with the Good Morning Wake Up Song! ☀️ Join Allie Alligator and Danny Duck for a cheerful morning sunrise routine in ABC Zoo.

Watch Allie and Danny stretch and get ready for a bright new day in this colorful kids animation. Follow along with morning stretches, making the bed, and positive morning vibes, making it easy for toddlers and preschoolers to start their day with a smile.

This interactive nursery rhyme is designed for preschool learning, helping children wake up happy and energized. Use this video to build a smooth, tear-free morning routine for daycare, preschool, and kindergarten.

🔔 Subscribe to ABC Zoo TV for more fun learning songs and toddler songs:
https://www.youtube.com/@ABCZooTv?sub_confirmation=1

⭐ Song Lyrics:
Good morning friends! The golden sun is up in the sky!
Allie and Danny are stretching and ready for a happy new day!
Wake up, wake up, stretch up high, touch the morning sun!
Make your bed and brush your teeth, today will be so fun!
Sunny day, smiling friends, hip hip hooray!
Can you stretch your arms all the way up? Stretch, stretch, stretch!
Great stretching! You are full of morning energy! High five!
See you next time with Henry Hippo! Bye-bye!

TIMESTAMPS:
0:00 - Good Morning Sunshine Intro
0:06 - Wake Up & Stretch High
0:18 - Making the Bed Routine
0:30 - Interactive Big Stretch Game
0:42 - Morning Energy High Five!

#ABCZooTV #GoodMorningSong #WakeUpSong #KidsAnimation #PreschoolLearning #MorningRoutine #ToddlerSongs #NurseryRhymes
""",
        "tags": [
            "Good Morning Wake Up Song for Kids", "good morning song", "wake up song for toddlers",
            "morning routine for kids", "preschool learning", "kids animation", "toddler songs",
            "ABC Zoo TV", "happy sunrise song", "kindergarten morning song", "nursery rhymes"
        ]
    },
    {
        "video_id": "g_oUn3ZdiQQ", # Day 26 (Letter Z)
        "ep_dir": BASE_DIR / "episodes/Ep_026_Letter_Z",
        "title": "Letter Z Phonics Song for Kids! 🎈 Learn Letter Z with Ziggy Zebra | ABC Zoo TV",
        "badge": "LETTER Z!",
        "sticker": "🎈 ZIPPER & ZEBRA",
        "ribbon": "PHONICS FOR KIDS",
        "description": """Can you find the zipper with Ziggy the Zebra? 🦓 Sing along and learn the Letter Z with ABC Zoo TV! ✨

Join Ziggy the Zebra for an exciting Letter Z learning adventure! Through a cheerful phonics song, toddlers practice the /z/ sound while discovering words like zipper and zigzag in colorful 3D clay animation.

This interactive experience is designed for preschool learning, helping children recognize letters and sounds easily. It's the perfect grand finale to our A-to-Z Phonics series!

🔔 Subscribe to ABC Zoo TV for more fun phonics and nursery rhymes:
https://www.youtube.com/@ABCZooTv?sub_confirmation=1

#ABCZooTV #LetterZ #LetterZSong #PhonicsSong #PreschoolLearning #ToddlerSongs #LearnABC #KidsAnimation #AlphabetSong
""",
        "tags": [
            "Letter Z Phonics Song for Kids", "letter z song", "learn letter z", "phonics letter z",
            "ziggy zebra", "ABC Zoo TV", "alphabet songs for children", "preschool learning",
            "toddler songs", "kids animation"
        ]
    },
    {
        "video_id": "mlFyUPWupY0", # Day 25 (Letter Y)
        "ep_dir": BASE_DIR / "episodes/Ep_025_Letter_Y",
        "title": "Letter Y Phonics Song for Kids! 🎈 Learn Letter Y with Yana the Yak | ABC Zoo TV",
        "badge": "LETTER Y!",
        "sticker": "🎈 YO-YO ADVENTURE",
        "ribbon": "PHONICS FOR KIDS",
        "description": """Can you find the yo-yo with Yana the Yak? 🐾 Sing along and learn the Letter Y with ABC Zoo TV! ✨

Join Yana the Yak for an exciting Letter Y adventure in the alpine meadow! Through a cheerful phonics song, toddlers practice the /y/ sound while playing with colorful spinning yo-yos in 3D clay animation.

This interactive lesson is designed for preschool and kindergarten learning, helping little ones recognize letters and develop phonemic awareness.

🔔 Subscribe to ABC Zoo TV for more fun phonics songs:
https://www.youtube.com/@ABCZooTv?sub_confirmation=1

#ABCZooTV #LetterY #LetterYSong #PhonicsSong #PreschoolLearning #ToddlerSongs #LearnABC #KidsAnimation #AlphabetSong
""",
        "tags": [
            "Letter Y Phonics Song for Kids", "letter y song", "learn letter y", "phonics letter y",
            "yana yak", "ABC Zoo TV", "alphabet songs for children", "preschool learning",
            "toddler songs", "kids animation"
        ]
    },
    {
        "video_id": "qQbOkhPnCnc", # Day 24 (Letter X)
        "ep_dir": BASE_DIR / "episodes/Ep_024_Letter_X",
        "title": "Letter X Phonics Song for Kids! 🎈 Xavier X-ray Fish Plays Xylophone | ABC Zoo TV",
        "badge": "LETTER X!",
        "sticker": "🎈 XYLOPHONE SONG",
        "ribbon": "PHONICS FOR KIDS",
        "description": """Can you find the xylophone with Xavier the X-ray Fish? 🐠 Sing along and learn the Letter X with ABC Zoo TV! ✨

Join Xavier the X-ray Fish for a glowing underwater musical adventure! Practice the /ks/ phonics sound with a colorful toy xylophone in 3D clay animation.

Designed for preschool and toddler learning, this video helps children master the tricky Letter X with music and fun visual games.

🔔 Subscribe to ABC Zoo TV for more educational kids songs:
https://www.youtube.com/@ABCZooTv?sub_confirmation=1

#ABCZooTV #LetterX #LetterXSong #PhonicsSong #PreschoolLearning #ToddlerSongs #LearnABC #KidsAnimation #AlphabetSong
""",
        "tags": [
            "Letter X Phonics Song for Kids", "letter x song", "learn letter x", "phonics letter x",
            "xavier x-ray fish", "ABC Zoo TV", "alphabet songs for children", "preschool learning",
            "toddler songs", "kids animation"
        ]
    }
]

def main():
    print("🚀 Starting Batch SEO & 16:9 Thumbnail Optimization...")
    thumb_generator = BASE_DIR / "scripts" / "generate_high_ctr_thumbnail.js"

    for item in EPISODES_TO_OPTIMIZE:
        ep_dir = item["ep_dir"]
        thumb_in = ep_dir / "thumbnail_hero.jpg"
        thumb_out = ep_dir / "high_ctr_thumbnail_16_9.jpg"

        print(f"\n========================================\nOptimizing {item['title'][:40]}...\n========================================")
        # 1. Render 16:9 high-CTR thumbnail
        cmd = [
            "node", str(thumb_generator),
            str(thumb_in),
            str(thumb_out),
            item["badge"],
            item["sticker"],
            item["ribbon"]
        ]
        subprocess.run(cmd, check=True)

        # 2. Update YouTube video metadata & thumbnail
        update_video_seo(
            video_id=item["video_id"],
            title=item["title"],
            description=item["description"],
            tags=item["tags"],
            thumbnail_path=str(thumb_out)
        )

    print("\n🎉 Batch optimization complete! All upcoming videos updated to 95+ vidIQ SEO standard and 16:9 thumbnails.")

if __name__ == "__main__":
    main()
