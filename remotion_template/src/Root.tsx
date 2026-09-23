import React from "react";
import { Composition } from "remotion";
import { ABCZooComposition } from "./Composition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 16:9 Landscape YouTube Video */}
      <Composition
        id="ABCZooLandscape"
        component={ABCZooComposition}
        durationInFrames={30 * 24} // 24 seconds at 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Letter A Song",
          characterName: "Allie Alligator",
          isShorts: false,
        }}
      />

      {/* 9:16 Vertical YouTube Shorts / TikTok */}
      <Composition
        id="ABCZooShorts"
        component={ABCZooComposition}
        durationInFrames={30 * 24}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          title: "Letter A Song",
          characterName: "Allie Alligator",
          isShorts: true,
        }}
      />
    </>
  );
};
