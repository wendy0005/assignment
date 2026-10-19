import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface Props {
  sectionNumber: number;
  totalSections: number;
  title: string;
}

export const SectionHeader: React.FC<Props> = ({
  sectionNumber,
  totalSections,
  title,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: {
      damping: 15,
    },
  });

  const translateY = interpolate(entrance, [0, 1], [-50, 0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  return (
    <div
      style={{
        position: "absolute",
        top: 40,
        left: 40,
        transform: `translateY(${translateY}px)`,
        opacity,
        display: "flex",
        alignItems: "center",
        gap: "16px",
        padding: "12px 24px",
        borderRadius: "16px",
        backgroundColor: "rgba(15, 23, 42, 0.85)",
        backdropFilter: "blur(12px)",
        border: "1px solid rgba(255, 255, 255, 0.15)",
        boxShadow: "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        zIndex: 10,
      }}
    >
      <div
        style={{
          background: "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
          color: "#ffffff",
          fontSize: "14px",
          fontWeight: 700,
          padding: "6px 12px",
          borderRadius: "8px",
          letterSpacing: "0.5px",
          textTransform: "uppercase",
        }}
      >
        Part {sectionNumber} / {totalSections}
      </div>

      <div
        style={{
          color: "#ffffff",
          fontSize: "20px",
          fontWeight: 600,
          fontFamily: "Inter, -apple-system, sans-serif",
          letterSpacing: "-0.02em",
        }}
      >
        {title}
      </div>
    </div>
  );
};
