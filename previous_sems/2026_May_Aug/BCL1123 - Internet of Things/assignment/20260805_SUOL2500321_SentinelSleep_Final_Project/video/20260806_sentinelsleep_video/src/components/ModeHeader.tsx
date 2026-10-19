import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface Props {
  sectionType: "explanation" | "demo";
}

export const ModeHeader: React.FC<Props> = ({ sectionType }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14 },
  });

  const translateY = interpolate(entrance, [0, 1], [-40, 0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  const isExplain = sectionType === "explanation";

  return (
    <div
      style={{
        position: "absolute",
        top: 20,
        left: "50%",
        transform: `translateX(-50%) translateY(${translateY}px)`,
        opacity,
        display: "flex",
        alignItems: "center",
        gap: "10px",
        padding: "8px 20px",
        borderRadius: "30px",
        backgroundColor: isExplain
          ? "rgba(30, 27, 75, 0.9)"
          : "rgba(6, 78, 59, 0.9)",
        backdropFilter: "blur(12px)",
        border: isExplain
          ? "1.5px solid rgba(129, 140, 248, 0.6)"
          : "1.5px solid rgba(52, 211, 153, 0.6)",
        boxShadow: isExplain
          ? "0 0 20px rgba(99, 102, 241, 0.4)"
          : "0 0 20px rgba(16, 185, 129, 0.4)",
        zIndex: 12,
      }}
    >
      <div
        style={{
          width: "10px",
          height: "10px",
          borderRadius: "50%",
          backgroundColor: isExplain ? "#818cf8" : "#34d399",
          boxShadow: isExplain ? "0 0 10px #818cf8" : "0 0 10px #34d399",
        }}
      />
      <span
        style={{
          color: "#ffffff",
          fontSize: "13px",
          fontWeight: 800,
          fontFamily: "Inter, sans-serif",
          letterSpacing: "1px",
          textTransform: "uppercase",
        }}
      >
        {isExplain
          ? "🎓 PRESENTATION MODE | CONCEPT EXPLANATION"
          : "⚡ LIVE DEMO MODE | REAL-TIME EXECUTION"}
      </span>
    </div>
  );
};
