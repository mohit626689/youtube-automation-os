import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Img,
  Audio,
  staticFile,
  spring,
} from "remotion";

interface Props {
  title: string;
  characterName: string;
  isShorts: boolean;
}

export const ABCZooComposition: React.FC<Props> = ({ isShorts }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 3 scenes, 8 seconds (240 frames) each = 720 frames total
  const sceneLength = 8 * fps;
  const currentSceneIndex = Math.floor(frame / sceneLength) % 3;
  const sceneFrame = frame % sceneLength;

  // Scene images
  const sceneImages = [
    "scene_01_hook.jpg",
    "scene_02_dancing.jpg",
    "scene_03_celebration.jpg",
  ];

  // Ken Burns zoom effect
  const zoom = interpolate(sceneFrame, [0, sceneLength], [1.0, 1.12], {
    extrapolateRight: "clamp",
  });

  // Bouncing letter badge spring
  const letterBounce = spring({
    frame: sceneFrame,
    fps,
    config: { damping: 10, mass: 0.5, stiffness: 100 },
  });

  // Subtitle lines based on timing
  const subtitles = [
    { start: 0, end: 3.5, text: "Hi friends! I'm Allie the Alligator!" },
    { start: 3.8, end: 7.5, text: "Look what I found... It's the Letter A!" },
    { start: 7.8, end: 11.5, text: "Can you say A with me? /a/ /a/ Apple!" },
    { start: 12.0, end: 15.5, text: "A is for Allie, playing every day!" },
    { start: 16.0, end: 19.5, text: "A is for Apple, hip hip hooray!" },
    { start: 20.0, end: 24.0, text: "Singing Letter A is a happy little treat!" },
  ];

  const currentSec = frame / fps;
  const currentSub = subtitles.find(
    (s) => currentSec >= s.start && currentSec <= s.end
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#29B6F6", overflow: "hidden" }}>
      {/* Background Audio */}
      <Audio src={staticFile("preview_melody.wav")} volume={0.9} />

      {/* Main Animated Scene Image */}
      <AbsoluteFill
        style={{
          transform: `scale(${zoom})`,
          transformOrigin: "center center",
        }}
      >
        <Img
          src={staticFile(sceneImages[currentSceneIndex])}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </AbsoluteFill>

      {/* Top Floating Phonics Badge */}
      <div
        style={{
          position: "absolute",
          top: isShorts ? 180 : 50,
          left: "50%",
          transform: `translateX(-50%) scale(${letterBounce})`,
          backgroundColor: "#FFD54F",
          border: "6px solid #1A237E",
          borderRadius: 40,
          padding: "12px 36px",
          boxShadow: "0 8px 24px rgba(0,0,0,0.3)",
          display: "flex",
          alignItems: "center",
          gap: 12,
        }}
      >
        <span
          style={{
            fontFamily: "Arial Rounded MT Bold, sans-serif",
            fontSize: isShorts ? 48 : 38,
            color: "#1A237E",
            fontWeight: "bold",
          }}
        >
          LETTER A 🍎
        </span>
      </div>

      {/* Synced Toddler Bubble Subtitles */}
      {currentSub && (
        <div
          style={{
            position: "absolute",
            bottom: isShorts ? 320 : 90,
            width: "100%",
            textAlign: "center",
            padding: "0 40px",
          }}
        >
          <div
            style={{
              display: "inline-block",
              backgroundColor: "rgba(26, 35, 126, 0.82)",
              borderRadius: 30,
              padding: "16px 36px",
              border: "4px solid #FFD54F",
              boxShadow: "0 10px 30px rgba(0,0,0,0.4)",
            }}
          >
            <span
              style={{
                fontFamily: "Arial Rounded MT Bold, sans-serif",
                fontSize: isShorts ? 44 : 52,
                color: "#FFFFFF",
                fontWeight: "900",
                textShadow: "3px 3px 0px #000000",
                letterSpacing: "0.5px",
              }}
            >
              {currentSub.text}
            </span>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
