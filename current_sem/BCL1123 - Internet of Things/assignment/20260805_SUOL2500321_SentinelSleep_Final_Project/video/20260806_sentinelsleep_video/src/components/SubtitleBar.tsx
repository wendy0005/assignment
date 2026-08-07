import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { VideoSection } from "../sectionsData";

interface Props {
  section: VideoSection;
}

export const SubtitleBar: React.FC<Props> = ({ section }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const activeSegment = section.timedSubtitles?.find(
    (item) => frame >= item.startFrame && frame <= item.endFrame
  );

  const activeSubtitle = activeSegment
    ? activeSegment.text
    : section.timedSubtitles?.[section.timedSubtitles.length - 1]?.text || section.transcript;

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14 },
  });

  const translateY = interpolate(entrance, [0, 1], [30, 0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  const hasPip = Boolean(section.pipImage || section.pipVideo);
  const subtitleWidth = hasPip ? "1040px" : "1480px";

  return (
    <div
      style={{
        position: "absolute",
        bottom: 30,
        left: 40,
        width: subtitleWidth,
        padding: "14px 24px",
        borderRadius: "16px",
        backgroundColor: "rgba(15, 23, 42, 0.92)",
        backdropFilter: "blur(16px)",
        border: "1px solid rgba(255, 255, 255, 0.12)",
        boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
        textAlign: "center",
        transform: `translateY(${translateY}px)`,
        opacity,
        zIndex: 10,
        transition: "width 0.3s ease-in-out",
      }}
    >
      <p
        style={{
          margin: 0,
          color: "#f8fafc",
          fontSize: "22px",
          lineHeight: "1.35",
          fontWeight: 600,
          fontFamily: "Inter, -apple-system, sans-serif",
          letterSpacing: "0.2px",
          textShadow: "0 2px 4px rgba(0, 0, 0, 0.8)",
        }}
      >
        "{activeSubtitle}"
      </p>
    </div>
  );
};
