import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface Props {
  keyPoints: string[];
  sectionType: "explanation" | "demo";
}

export const KeyPointsCard: React.FC<Props> = ({ keyPoints, sectionType }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: Math.max(0, frame - 10),
    fps,
    config: { damping: 16 },
  });

  const translateX = interpolate(entrance, [0, 1], [40, 0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  if (!keyPoints || keyPoints.length === 0) return null;

  const isExplain = sectionType === "explanation";

  return (
    <div
      style={{
        position: "absolute",
        top: 80,
        right: 30,
        width: "330px",
        padding: "14px 18px",
        borderRadius: "14px",
        backgroundColor: isExplain
          ? "rgba(15, 23, 42, 0.90)"
          : "rgba(15, 23, 42, 0.85)",
        backdropFilter: "blur(12px)",
        border: isExplain
          ? "1px solid rgba(129, 140, 248, 0.4)"
          : "1px solid rgba(59, 130, 246, 0.3)",
        boxShadow: "0 8px 24px rgba(0, 0, 0, 0.5)",
        transform: `translateX(${translateX}px)`,
        opacity,
        zIndex: 11,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "6px",
          marginBottom: "10px",
        }}
      >
        <span
          style={{
            fontSize: "11px",
            fontWeight: 800,
            color: isExplain ? "#a5b4fc" : "#60a5fa",
            textTransform: "uppercase",
            letterSpacing: "0.8px",
          }}
        >
          {isExplain ? "📋 EXPLANATION HIGHLIGHTS" : "🎯 LIVE DEMO OBJECTIVES"}
        </span>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        {keyPoints.map((point, idx) => {
          const itemEntrance = spring({
            frame: Math.max(0, frame - 12 - idx * 3),
            fps,
            config: { damping: 18 },
          });

          return (
            <div
              key={idx}
              style={{
                display: "flex",
                alignItems: "flex-start",
                gap: "8px",
                transform: `translateX(${interpolate(itemEntrance, [0, 1], [15, 0])}px)`,
                opacity: itemEntrance,
              }}
            >
              <div
                style={{
                  width: "6px",
                  height: "6px",
                  borderRadius: "50%",
                  backgroundColor: isExplain ? "#818cf8" : "#3b82f6",
                  marginTop: "5px",
                  flexShrink: 0,
                  boxShadow: isExplain ? "0 0 6px #818cf8" : "0 0 6px #3b82f6",
                }}
              />
              <span
                style={{
                  color: "#f1f5f9",
                  fontSize: "13px",
                  fontWeight: 500,
                  lineHeight: "1.3",
                  fontFamily: "Inter, sans-serif",
                }}
              >
                {point}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
