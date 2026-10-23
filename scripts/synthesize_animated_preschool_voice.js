const fs = require('fs');
const path = require('path');
const { MsEdgeTTS, OUTPUT_FORMAT, ProsodyOptions } = require('msedge-tts');

async function synthesizeLine(tts, text, outDir, fileName, prosody) {
  const lineDir = path.join(outDir, `_line_${fileName}`);
  if (!fs.existsSync(lineDir)) fs.mkdirSync(lineDir, { recursive: true });
  
  await tts.toFile(lineDir, text, prosody);
  const generatedPath = path.join(lineDir, 'audio.mp3');
  const targetPath = path.join(outDir, `${fileName}.mp3`);
  
  fs.copyFileSync(generatedPath, targetPath);
  fs.rmSync(lineDir, { recursive: true, force: true });
  return targetPath;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("Usage: node synthesize_animated_preschool_voice.js <episode_dir> <lines_json_file> [voice_name]");
    process.exit(1);
  }

  const epDir = path.resolve(args[0]);
  const linesFile = path.resolve(args[1]);
  const voiceName = args[2] || 'en-US-AnaNeural';

  if (!fs.existsSync(linesFile)) {
    console.error(`Lines file not found: ${linesFile}`);
    process.exit(1);
  }

  const lines = JSON.parse(fs.readFileSync(linesFile, 'utf8'));
  console.log(`🎙️ Synthesizing animated preschool voice (${lines.length} lines) with pitch/rate prosody using: ${voiceName}`);

  const voiceOutDir = path.join(epDir, 'neural_vocals');
  if (!fs.existsSync(voiceOutDir)) fs.mkdirSync(voiceOutDir, { recursive: true });

  const tts = new MsEdgeTTS();
  await tts.setMetadata(voiceName, OUTPUT_FORMAT.AUDIO_24KHZ_96KBITRATE_MONO_MP3);

  // Upbeat, warm child prosody: slightly higher pitch (+12Hz) and bouncy pacing (+4%)
  const prosody = new ProsodyOptions();
  prosody.pitch = "+15Hz";
  prosody.rate = 1.05;
  prosody.volume = 100.0;

  const results = [];
  for (let i = 0; i < lines.length; i++) {
    const text = typeof lines[i] === 'string' ? lines[i] : lines[i].text;
    const fileName = `ana_seg_${i}`;
    console.log(`  [${i+1}/${lines.length}] Voice: "${text}"`);
    const mp3Path = await synthesizeLine(tts, text, voiceOutDir, fileName, prosody);
    results.push({
      index: i,
      text: text,
      file: mp3Path
    });
  }

  const manifestPath = path.join(voiceOutDir, 'voice_manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(results, null, 2));
  console.log(`✨ Successfully generated cheerful animated voice lines at: ${voiceOutDir}`);
}

main().catch(err => {
  console.error("Error synthesizing voice:", err);
  process.exit(1);
});
