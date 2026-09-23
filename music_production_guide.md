# ABC Zoo TV — AI Music & Vocal Production Guide

This guide provides exact, battle-tested prompt syntax and audio settings for synthesizing professional, catchy, broadcast-quality preschool songs using **Suno AI**, **Udio**, and **ElevenLabs**.

---

## 1. Suno AI & Udio Prompt Architecture

To produce songs that hold a toddler's attention without fatiguing parents, the audio must feature clean acoustic instrumentation, bright percussion, and a bouncy tempo.

### Recommended Suno/Udio Style Prompt (Copy-Paste)
```text
nursery rhyme, preschool kids song, cheerful acoustic ukulele, marimba, glockenspiel, playful walking bass, soft handclaps, bright female soprano children's singer, enthusiastic, bouncy rhythm, clean articulation, 112 BPM, kindergarten singalong, high production quality
```

### Suno Meta-Tags & Song Formatting Structure
Always use structural bracket tags in your Suno / Udio custom lyrics box to dictate tempo changes and call-and-response dynamics:

* `[Intro: Playful marimba roll, xylophone slide, giggle]`
* `[Verse 1: Bouncy acoustic ukulele and claps]`
* `[Pre-Chorus: Ascending melodic bell chime]`
* `[Chorus: Energetic, danceable, driving beat, vocal harmonizing]`
* `[Bridge: Soft rhythmic tick-tock thinking music]`
* `[Celebration Drop: Tambourines and joyful cheer "Yay!"]`
* `[Outro: Gentle ukulele fadeout and character wave]`

---

## 2. Episode 1 Production Package: Letter A (Allie Alligator)

### Suno AI Custom Lyrics (Ready to Generate)

```text
[Intro: Playful ascending xylophone slide, bubbly bounce]
Hi friends! I'm Allie the Alligator! 
Look what I found... It's the Letter A!
Can you say A with me? 
/a/ /a/ Apple!

[Verse 1: Upbeat acoustic ukulele with steady claps, 112 BPM]
A is for Allie, playing every day!
A is for Apple, hip hip hooray!
/a/ /a/ Apple, crunchy and sweet,
Singing Letter A is a happy little treat!

[Chorus: High energy, marimba swell, danceable groove]
A, A, A! Let's jump up high!
Reach for the apple in the sunny sky!
Wiggle your toes and clap with cheer,
The happy Letter A is finally here!

[Bridge: Playful interactive thinking beat, soft woodblock tick-tock]
Which one starts with /a/? 
Is it a Shoe, or a yummy Apple?
Point to the apple!
[Chime Sound: Ding!]
You found it! You're so smart! High five!

[Verse 2: Full celebration, tambourines and sunny energy]
A is for Airplane, flying in the air!
A is for Astronaut, floating way up there!
A, A, A, sing it loud and proud,
Sing with Allie to the whole zoo crowd!

[Outro: Soft ukulele strum, fade out]
Yay! You learned Letter A!
See you next time with my best friend Barnaby!
Bye-bye!
```

---

## 3. ElevenLabs Vocal Synthesis Configuration

For spoken character intros, phonics letter sounds, and interactive callouts:

* **Recommended Voices:**
  * `Lily` (Velvety, warm, natural female preschool narrator)
  * `Freya` (Clear, youthful, enthusiastic)
  * `Charlie` (Cheerful energetic child voice)
* **Voice Settings:**
  * **Stability:** `0.45` (Lower stability increases expressive, animated emotion suitable for kids)
  * **Clarity / Similarity:** `0.80` (Preserves crisp phonetic consonant pronunciation like `/a/`, `/b/`, `/k/`)
  * **Style Exaggeration:** `0.20` (Adds playful theatricality without introducing artifacts)
  * **Speaker Boost:** `Enabled` (Boosts presence in the audio mix)

---

## 4. Audio Mixing Standards for YouTube Kids

1. **Integrated Loudness:** Target `-14 LUFS` (standard YouTube normalization target).
2. **Vocal Presence:** Keep the lead vocal `+2.5 dB` above the backing music so toddlers can clearly distinguish phonetic sounds on mobile phone speakers and low-end tablets.
3. **High-Frequency Rolloff:** Gently roll off frequencies above `14 kHz` to avoid harsh sibilance or ear fatigue for sensitive toddler hearing.
