import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

interface Props {
  transcript: string;
  presenterName?: string;
  durationInFrames?: number;
}

export function getActiveSubtitleChunk(
  fullTranscript: string,
  totalFrames: number,
  currentFrame: number
): string {
  const sentences = fullTranscript
    .split(/(?<=[.!?])\s+/)
    .filter((s) => s.trim().length > 0);

  if (sentences.length <= 1) return fullTranscript;

  const framesPerSentence = totalFrames / sentences.length;
  const activeIndex = Math.min(
    sentences.length - 1,
    Math.floor(currentFrame / framesPerSentence)
  );

  return sentences[activeIndex];
}

export const AvatarPresenter: React.FC<Props> = ({
  transcript,
  presenterName = "Chan Jing Yi",
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames: configDuration } = useVideoConfig();

  const totalFrames = durationInFrames || configDuration || 300;
  const activeSubtitle = getActiveSubtitleChunk(transcript, totalFrames, frame);

  const entrance = spring({
    frame,
    fps,
    config: { damping: 15 },
  });

  const translateY = interpolate(entrance, [0, 1], [30, 0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  const pulse = Math.sin(frame * 0.15) * 0.02 + 1;

  // 5 mini audio bars
  const audioBars = Array.from({ length: 5 }).map((_, i) => {
    const speed = 0.2 + (i % 3) * 0.08;
    const height = 4 + Math.abs(Math.sin((frame + i * 3) * speed)) * 12;
    return height;
  });

  return (
    <>
      {/* Low-profile Subtitle Text Bar at Bottom Center/Left */}
      <div
        style={{
          position: "absolute",
          bottom: 24,
          left: 40,
          right: 280,
          padding: "10px 20px",
          borderRadius: "14px",
          backgroundColor: "rgba(15, 23, 42, 0.85)",
          backdropFilter: "blur(12px)",
          border: "1px solid rgba(255, 255, 255, 0.12)",
          boxShadow: "0 8px 24px rgba(0, 0, 0, 0.4)",
          transform: `translateY(${translateY}px)`,
          opacity,
          zIndex: 14,
          pointerEvents: "none",
        }}
      >
        <p
          style={{
            margin: 0,
            color: "#f8fafc",
            fontSize: "20px",
            lineHeight: "1.35",
            fontWeight: 600,
            fontFamily: "Inter, -apple-system, sans-serif",
            textShadow: "0 1px 3px rgba(0, 0, 0, 0.8)",
          }}
        >
          "{activeSubtitle}"
        </p>
      </div>

      {/* Subtle Avatar Presenter Badge at Bottom Right Corner */}
      <div
        style={{
          position: "absolute",
          bottom: 24,
          right: 30,
          display: "flex",
          alignItems: "center",
          gap: "10px",
          padding: "6px 12px 6px 6px",
          borderRadius: "30px",
          backgroundColor: "rgba(15, 23, 42, 0.90)",
          backdropFilter: "blur(12px)",
          border: "1.5px solid rgba(59, 130, 246, 0.5)",
          boxShadow: "0 6px 20px rgba(0, 0, 0, 0.5)",
          transform: `translateY(${translateY}px)`,
          opacity,
          zIndex: 15,
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            position: "relative",
            width: "46px",
            height: "46px",
            borderRadius: "50%",
            padding: "2px",
            background: "linear-gradient(135deg, #3b82f6, #60a5fa)",
            boxShadow: "0 0 10px rgba(59, 130, 246, 0.5)",
            transform: `scale(${pulse})`,
            flexShrink: 0,
          }}
        >
          <img
            src={staticFile("avatar.jpg")}
            alt="AI Presenter"
            style={{
              width: "100%",
              height: "100%",
              borderRadius: "50%",
              objectFit: "cover",
            }}
          />
          <div
            style={{
              position: "absolute",
              bottom: 1,
              right: 1,
              width: "9px",
              height: "9px",
              borderRadius: "50%",
              backgroundColor: "#22c55e",
              border: "2px solid #0f172a",
            }}
          />
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "2px" }}>
          <div
            style={{
              color: "#ffffff",
              fontSize: "12px",
              fontWeight: 700,
              fontFamily: "Inter, sans-serif",
              whiteSpace: "nowrap",
            }}
          >
            {presenterName}
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "3px",
              height: "12px",
            }}
          >
            {audioBars.map((height, idx) => (
              <div
                key={idx}
                style={{
                  width: "3px",
                  height: `${height}px`,
                  backgroundColor: "#60a5fa",
                  borderRadius: "2px",
                }}
              />
            ))}
          </div>
        </div>
      </div>
    </>
  );
};
