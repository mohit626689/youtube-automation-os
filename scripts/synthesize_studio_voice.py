#!/usr/bin/env python3
"""
ABC Zoo TV — Studio Neural Voiceover Engine
Supports 4 tiers of broadcast-quality preschool voiceover:
  1. Edge-TTS Neural Child Voices (100% Free, no API key needed):
     - 'en-US-AnaNeural' (Sweet, authentic, expressive 5-year-old American child)
     - 'en-GB-MaisieNeural' (Sweet British child)
     - 'en-US-JennyNeural' (Warm, friendly preschool teacher / mother)
  2. ElevenLabs Voice AI (Studio Disney/Pixar tier, requires ELEVENLABS_API_KEY)
  3. OpenAI TTS (Clear & articulate, requires OPENAI_API_KEY)
  4. Audio Intake: Drop your own Suno/Udio song or human recording directly
"""

import os
import sys
import json
import asyncio
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def synthesize_with_edge_tts(text, output_file, voice="en-US-AnaNeural", rate="+0%", pitch="+0Hz"):
    """
    Uses Microsoft Edge's Neural TTS to generate ultra-realistic child voices.
    """
    try:
        import edge_tts
    except ImportError:
        # Try running via CLI if installed, or install guidance
        raise ImportError(
            "edge-tts package is required for free neural child voices.\n"
            "To install, run: pip install edge-tts"
        )
        
    async def _generate():
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(str(output_file))

    asyncio.run(_generate())
    print(f"✨ Synthesized neural child voice ({voice}): {output_file.name}")
    return output_file

def synthesize_with_openai(text, output_file, api_key=None, voice="nova", model="tts-1-hd"):
    """
    Uses OpenAI's high-definition text-to-speech API.
    """
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is not set.")
        
    import urllib.request
    
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "input": text,
        "voice": voice, # nova or shimmer
        "response_format": "mp3"
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req) as resp:
        with open(output_file, "wb") as f:
            f.write(resp.read())
            
    print(f"✨ Synthesized OpenAI HD voice ({voice}): {output_file.name}")
    return output_file

def synthesize_with_elevenlabs(text, output_file, api_key=None, voice_id="EXAVITQu4vr4xnSDxMaL"):
    """
    Uses ElevenLabs API for cinema-grade preschool voices.
    Default voice_id: 'Bella' or 'Lily'
    """
    key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY is not set.")
        
    import urllib.request
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.85,
            "style": 0.25
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req) as resp:
        with open(output_file, "wb") as f:
            f.write(resp.read())
            
    print(f"✨ Synthesized ElevenLabs studio voice: {output_file.name}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description="ABC Zoo TV Studio Voice Generator")
    parser.add_argument("--backend", choices=["edge", "openai", "elevenlabs"], default="edge", help="TTS Backend")
    parser.add_argument("--voice", type=str, default="en-US-AnaNeural", help="Voice model/name")
    parser.add_argument("--text", type=str, required=True, help="Text to speak")
    parser.add_argument("--output", type=str, required=True, help="Output audio file path")
    args = parser.parse_args()
    
    out_path = Path(args.output)
    
    if args.backend == "edge":
        synthesize_with_edge_tts(args.text, out_path, voice=args.voice)
    elif args.backend == "openai":
        synthesize_with_openai(args.text, out_path, voice=args.voice)
    elif args.backend == "elevenlabs":
        synthesize_with_elevenlabs(args.text, out_path, voice_id=args.voice)

if __name__ == "__main__":
    main()
