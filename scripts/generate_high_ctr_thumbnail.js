const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

async function renderThumbnail({
  imagePath,
  outputPath,
  badgeText = "ABC PHONICS!",
  stickerText = "🎈 LEARN A-Z!",
  titleText = "SING & DANCE"
}) {
  const chromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  if (!fs.existsSync(chromePath)) {
    throw new Error(`Chrome not found at ${chromePath}`);
  }

  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });

  // Read base image and convert to base64
  const imgBuffer = fs.readFileSync(imagePath);
  const imgBase64 = `data:image/jpeg;base64,${imgBuffer.toString('base64')}`;

  const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1280px;
    height: 720px;
    overflow: hidden;
    background: #000;
    font-family: "Arial Rounded MT Bold", -apple-system, sans-serif;
  }
  .container {
    position: relative;
    width: 1280px;
    height: 720px;
    overflow: hidden;
  }
  /* Background layer */
  .bg-layer {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    background-image: url('${imgBase64}');
    background-size: cover;
    background-position: center 30%;
    filter: saturate(1.2) contrast(1.08) brightness(1.02);
    transform: scale(1.02);
  }
  /* Subtle vignette gradient overlay */
  .vignette {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.35) 100%);
    pointer-events: none;
  }
  /* Top-left High-CTR badge */
  .badge-main {
    position: absolute;
    top: 40px;
    left: 48px;
    background: linear-gradient(135deg, #FFF176 0%, #FFD600 40%, #FF6D00 100%);
    border: 5px solid #FFFFFF;
    border-radius: 9999px;
    padding: 16px 42px;
    display: inline-flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 14px 35px rgba(0,0,0,0.65), 0 0 30px rgba(255, 214, 0, 0.55);
  }
  .badge-text {
    font-size: 52px;
    font-weight: 900;
    color: #1A237E;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    text-shadow: 0 2px 0 rgba(255,255,255,0.6);
  }
  /* Top-right Action Sticker */
  .badge-sticker {
    position: absolute;
    top: 44px;
    right: 48px;
    background: linear-gradient(135deg, #00E676 0%, #00C853 100%);
    border: 4.5px solid #FFFFFF;
    border-radius: 9999px;
    padding: 14px 36px;
    display: inline-flex;
    align-items: center;
    box-shadow: 0 14px 35px rgba(0,0,0,0.65), 0 0 25px rgba(0, 230, 118, 0.45);
  }
  .sticker-text {
    font-size: 38px;
    font-weight: 900;
    color: #FFFFFF;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    text-shadow: 0 3px 6px rgba(0,0,0,0.5);
  }
  /* Bottom High-Impact Ribbon */
  .bottom-ribbon {
    position: absolute;
    bottom: 35px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(13, 27, 42, 0.92);
    backdrop-filter: blur(12px);
    border: 4.5px solid #FFD600;
    border-radius: 9999px;
    padding: 14px 50px;
    box-shadow: 0 16px 40px rgba(0,0,0,0.75), 0 0 30px rgba(255, 214, 0, 0.4);
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .ribbon-text {
    font-size: 40px;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .ribbon-highlight {
    color: #00E5FF;
    margin-left: 10px;
    text-shadow: 0 0 15px rgba(0, 229, 255, 0.7);
  }
</style>
</head>
<body>
<div class="container">
  <div class="bg-layer"></div>
  <div class="vignette"></div>

  <div class="badge-main">
    <span class="badge-text">${badgeText}</span>
  </div>

  <div class="badge-sticker">
    <span class="sticker-text">${stickerText}</span>
  </div>

  <div class="bottom-ribbon">
    <span class="ribbon-text">${titleText}</span>
    <span class="ribbon-highlight">⭐ 4K HD</span>
  </div>
</div>
</body>
</html>`;

  await page.setContent(html, { waitUntil: 'load' });
  await page.screenshot({ path: outputPath, type: 'jpeg', quality: 95 });
  await browser.close();

  console.log(`✨ Generated high-CTR 16:9 thumbnail: ${outputPath}`);
}

// CLI support
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("Usage: node generate_high_ctr_thumbnail.js <image_path> <output_path> [badge] [sticker] [ribbon]");
    process.exit(1);
  }
  renderThumbnail({
    imagePath: path.resolve(args[0]),
    outputPath: path.resolve(args[1]),
    badgeText: args[2] || "ABC PHONICS!",
    stickerText: args[3] || "🎈 LEARN A-Z!",
    titleText: args[4] || "SING & DANCE"
  }).catch(err => {
    console.error("Error generating thumbnail:", err);
    process.exit(1);
  });
}

module.exports = { renderThumbnail };
