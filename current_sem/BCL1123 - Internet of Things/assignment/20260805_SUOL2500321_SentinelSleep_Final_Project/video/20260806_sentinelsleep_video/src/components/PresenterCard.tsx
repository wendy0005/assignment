import React from "react";
import { OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

interface Props {
  videoFile: string;
}

export const PresenterCard: React.FC<Props> = ({ videoFile }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 15 },
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 30,
        right: 40,
        width: "300px",
        height: "533px", // 9:16 aspect ratio matching 720x1280
        borderRadius: "20px",
        overflow: "hidden",
        backgroundColor: "#090d16",
        border: "2px solid rgba(59, 130, 246, 0.5)",
        boxShadow: "0 16px 40px rgba(0, 0, 0, 0.7), 0 0 25px rgba(59, 130, 246, 0.2)",
        transform: `scale(${entrance})`,
        opacity: entrance,
        zIndex: 15,
      }}
    >
      {/* Top Header Tag */}
      <div
        style={{
          position: "absolute",
          top: 10,
          left: 12,
          display: "flex",
          alignItems: "center",
          gap: "6px",
          backgroundColor: "rgba(15, 23, 42, 0.85)",
          backdropFilter: "blur(8px)",
          padding: "4px 10px",
          borderRadius: "12px",
          border: "1px solid rgba(255, 255, 255, 0.15)",
          zIndex: 2,
        }}
      >
        <div
          style={{
            width: "8px",
            height: "8px",
            borderRadius: "50%",
            backgroundColor: "#22c55e",
            boxShadow: "0 0 6px #22c55e",
          }}
        />
        <span
          style={{
            color: "#ffffff",
            fontSize: "11px",
            fontWeight: 700,
            fontFamily: "Inter, sans-serif",
            letterSpacing: "0.5px",
          }}
        >
          PRESENTER
        </span>
      </div>

      {/* Vertical 9:16 Presenter Video */}
      <OffthreadVideo
        src={staticFile(videoFile)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />
    </div>
  );
};
