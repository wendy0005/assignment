import React from "react";
import { OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { VideoSection } from "../sectionsData";

interface Props {
  section: VideoSection;
}

export const OverlayCard: React.FC<Props> = ({ section }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 16 },
  });

  const pipImage = section.pipImage;
  const pipVideo = section.pipVideo;
  const pipVideo2 = section.pipVideo2;

  if (!pipImage && !pipVideo && !pipVideo2) return null;

  return (
    <div
      style={{
        position: "absolute",
        top: 120,
        right: 380, // Positioned beside Presenter Card with high prominence
        width: "420px",
        height: "760px",
        borderRadius: "24px",
        overflow: "hidden",
        backgroundColor: "#080d1a",
        border: "2px solid rgba(59, 130, 246, 0.7)",
        boxShadow: "0 20px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(59, 130, 246, 0.3)",
        transform: `scale(${entrance})`,
        opacity: entrance,
        zIndex: 14,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Top Header Banner */}
      <div
        style={{
          height: "36px",
          backgroundColor: "rgba(37, 99, 235, 0.95)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 14px",
          color: "#ffffff",
          fontSize: "12px",
          fontWeight: 800,
          fontFamily: "Inter, sans-serif",
          letterSpacing: "0.5px",
          textTransform: "uppercase",
          flexShrink: 0,
        }}
      >
        <span>📱 Blynk Cloud Live Sync</span>
        <span style={{ fontSize: "10px", opacity: 0.85 }}>Mobile Telemetry</span>
      </div>

      {/* High-Resolution Mobile Dashboard Content */}
      <div
        style={{
          flex: 1,
          backgroundColor: "#020617",
          position: "relative",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          overflow: "hidden",
        }}
      >
        {pipImage && (
          <img
            src={staticFile(pipImage)}
            alt="Blynk Mobile Visual"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
            }}
          />
        )}

        {/* Case 1: Single PIP Video */}
        {pipVideo && !pipVideo2 && (
          <OffthreadVideo
            src={staticFile(pipVideo)}
            muted
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
            }}
          />
        )}

        {/* Case 2: Multi-Video PIP Sequencing (e.g. Section 12 Gas Alert -> Acknowledge Alert) */}
        {pipVideo && pipVideo2 && (
          <>
            <Sequence durationInFrames={570}>
              <OffthreadVideo
                src={staticFile(pipVideo)}
                muted
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "contain",
                }}
              />
            </Sequence>
            <Sequence from={570}>
              <OffthreadVideo
                src={staticFile(pipVideo2)}
                muted
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "contain",
                }}
              />
            </Sequence>
          </>
        )}
      </div>
    </div>
  );
};
