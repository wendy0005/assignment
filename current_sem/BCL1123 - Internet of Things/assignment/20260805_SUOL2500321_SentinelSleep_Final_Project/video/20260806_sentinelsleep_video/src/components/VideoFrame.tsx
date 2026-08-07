import React from "react";
import { OffthreadVideo, staticFile } from "remotion";

interface Props {
  videoFile: string;
}

export const VideoFrame: React.FC<Props> = ({ videoFile }) => {
  return (
    <div
      style={{
        width: "1480px",
        height: "830px",
        borderRadius: "20px",
        backgroundColor: "#090d16",
        border: "1.5px solid rgba(255, 255, 255, 0.12)",
        boxShadow: "0 25px 60px rgba(0, 0, 0, 0.8), 0 0 30px rgba(59, 130, 246, 0.15)",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        position: "relative",
      }}
    >
      {/* Window Title Bar */}
      <div
        style={{
          height: "38px",
          backgroundColor: "#0f172a",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
          display: "flex",
          alignItems: "center",
          padding: "0 16px",
          gap: "8px",
          position: "relative",
        }}
      >
        <div style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#ef4444" }} />
        <div style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#f59e0b" }} />
        <div style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#10b981" }} />

        <div
          style={{
            position: "absolute",
            left: "50%",
            transform: "translateX(-50%)",
            color: "#64748b",
            fontSize: "12px",
            fontWeight: 600,
            fontFamily: "Inter, monospace",
            letterSpacing: "0.5px",
          }}
        >
          SentinelSleep Demonstration Feed — {videoFile.split("/").pop()}
        </div>
      </div>

      {/* Video Content Viewport */}
      <div
        style={{
          flex: 1,
          position: "relative",
          backgroundColor: "#000000",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          overflow: "hidden",
        }}
      >
        <OffthreadVideo
          src={staticFile(videoFile)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
          }}
        />
      </div>
    </div>
  );
};
