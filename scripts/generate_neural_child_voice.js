const fs = require('fs');
const path = require('path');
const { MsEdgeTTS, OUTPUT_FORMAT } = require('msedge-tts');

async function synthesizeLine(tts, text, outDir, fileName) {
  const lineDir = path.join(outDir, `_line_${fileName}`);
  if (!fs.existsSync(lineDir)) fs.mkdirSync(lineDir, { recursive: true });
  
  await tts.toFile(lineDir, text);
  const generatedPath = path.join(lineDir, 'audio.mp3');
  const targetPath = path.join(outDir, `${fileName}.mp3`);
  
  fs.copyFileSync(generatedPath, targetPath);
  fs.rmSync(lineDir, { recursive: true, force: true });
  return targetPath;
}

async function main() {
  const args = process.argv.slice(2);
  const epDir = args[0] ? path.resolve(args[0]) : path.resolve(__dirname, '../episodes/Ep_001_Letter_A');
  const voiceName = args[1] || 'en-US-AnaNeural';

  console.log(`🎙️ Synthesizing Studio Neural Child Voice using: ${voiceName}`);
  console.log(`📁 Target Directory: ${epDir}`);

  let letter = 'A';
  const match = epDir.match(/Letter_([A-Z])/i);
  if (match) letter = match[1].toUpperCase();

  const configPath = path.resolve(__dirname, '../pipeline_config.json');
  let charName = "Allie", animal = "Alligator", obj = "Apple", nextChar = "Barnaby", nextLetter = "B";
  
  if (fs.existsSync(configPath)) {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    if (config.characters && config.characters[letter]) {
      const c = config.characters[letter];
      charName = c.name;
      animal = c.animal;
      obj = c.primary_objects[0];
      
      const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      const nextIdx = (alphabet.indexOf(letter) + 1) % 26;
      nextLetter = alphabet[nextIdx];
      if (config.characters[nextLetter]) {
        nextChar = config.characters[nextLetter].name;
      }
    }
  }

  const lines = [
    { text: `Hi friends! I am ${charName} the ${animal}!`, start: 0.2 },
    { text: `Look what I found... It is the Letter ${letter}!`, start: 3.2 },
    { text: `Can you say ${letter} with me? ${letter}! ${letter}! ${obj}!`, start: 6.8 },
    { text: `${letter} is for ${charName}, playing every day!`, start: 10.8 },
    { text: `${letter} is for ${obj}, hip hip hooray!`, start: 14.2 },
    { text: `Can you find the ${obj.toLowerCase()}? Point to it!`, start: 17.5 },
    { text: `You found it! Good job! High five!`, start: 20.8 },
    { text: `See you next time with ${nextChar}! Bye-bye!`, start: 23.8 }
  ];

  const tts = new MsEdgeTTS();
  await tts.setMetadata(voiceName, OUTPUT_FORMAT.AUDIO_24KHZ_96KBITRATE_MONO_MP3);

  const voiceOutDir = path.join(epDir, 'neural_vocals');
  if (!fs.existsSync(voiceOutDir)) fs.mkdirSync(voiceOutDir, { recursive: true });

  const results = [];
  for (let i = 0; i < lines.length; i++) {
    const item = lines[i];
    const fileName = `ana_seg_${i}`;
    console.log(`  [${i+1}/${lines.length}] Synthesizing: "${item.text}"`);
    const mp3Path = await synthesizeLine(tts, item.text, voiceOutDir, fileName);
    results.push({
      index: i,
      text: item.text,
      start: item.start,
      file: mp3Path
    });
  }

  const manifestPath = path.join(voiceOutDir, 'voice_manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(results, null, 2));
  console.log(`✨ All ${lines.length} neural voice lines generated successfully at: ${voiceOutDir}`);
}

main().catch(err => {
  console.error("Error synthesizing neural voice:", err);
  process.exit(1);
});
