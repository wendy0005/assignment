import React from "react";
import { interpolate, OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { VideoSection } from "../sectionsData";

interface Props {
  section: VideoSection;
}

export const MainProjectDisplay: React.FC<Props> = ({ section }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 16 },
  });

  const isExplain = section.sectionType === "explanation";
  const hasPip = Boolean(section.pipImage || section.pipVideo);
  const isSection13 = section.id === "13_network_security";

  // Dynamically scale width so side-by-side Blynk Cloud card fits with zero overlap
  const viewportWidth = hasPip ? "1040px" : "1480px";

  // Determine active code highlight phase for Section 13 based on spoken speech audio frame
  const activeHighlightStep =
    frame < 255 ? "local_loop" : frame < 465 ? "reconnect" : "secrets";

  return (
    <div
      style={{
        position: "absolute",
        top: 100,
        left: 40,
        width: viewportWidth,
        height: "820px",
        borderRadius: "24px",
        overflow: "hidden",
        backgroundColor: "#080d1a",
        border: isExplain
          ? "1.5px solid rgba(129, 140, 248, 0.3)"
          : "1.5px solid rgba(59, 130, 246, 0.3)",
        boxShadow: "0 20px 60px rgba(0, 0, 0, 0.7), 0 0 30px rgba(15, 23, 42, 0.8)",
        transform: `scale(${entrance})`,
        opacity: entrance,
        display: "flex",
        flexDirection: "column",
        zIndex: 5,
        transition: "width 0.3s ease-in-out",
      }}
    >
      {/* Visual Material Case: Display Wokwi Circuit / Blynk App Screen in Full Resolution */}
      {section.overlayImage ? (
        <div
          style={{
            width: "100%",
            height: "100%",
            backgroundColor: "#020617",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "20px",
          }}
        >
          <img
            src={staticFile(section.overlayImage)}
            alt="Project Visual Material"
            style={{
              maxWidth: "100%",
              maxHeight: "100%",
              objectFit: "contain",
              borderRadius: "12px",
            }}
          />
        </div>
      ) : section.overlayVideo ? (
        <div
          style={{
            width: "100%",
            height: "100%",
            backgroundColor: "#020617",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {section.overlayVideo2 ? (
            /* Multi-video sequence (e.g. Part 5 Temperature Fan -> Humidity Warning) */
            <>
              <Sequence durationInFrames={500}>
                <OffthreadVideo
                  src={staticFile(section.overlayVideo)}
                  muted
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                  }}
                />
              </Sequence>
              <Sequence from={500}>
                <OffthreadVideo
                  src={staticFile(section.overlayVideo2)}
                  muted
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                  }}
                />
              </Sequence>
            </>
          ) : (
            <OffthreadVideo
              src={staticFile(section.overlayVideo)}
              muted
              style={{
                width: "100%",
                height: "100%",
                objectFit: "contain",
              }}
            />
          )}
        </div>
      ) : isSection13 ? (
        /* Code & Serial Monitor Technical Presentation Viewport for Section 13 with Animated Code Highlighting */
        <div
          style={{
            width: "100%",
            height: "100%",
            padding: "36px 48px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            background: "radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 0.98) 0%, rgba(2, 6, 23, 1) 100%)",
          }}
        >
          {/* Header */}
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <div>
              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "4px 14px",
                  borderRadius: "20px",
                  backgroundColor: "rgba(99, 102, 241, 0.15)",
                  border: "1px solid rgba(129, 140, 248, 0.4)",
                  color: "#a5b4fc",
                  fontSize: "12px",
                  fontWeight: 700,
                  letterSpacing: "1px",
                  textTransform: "uppercase",
                  marginBottom: "8px",
                }}
              >
                🔒 NETWORK RESILIENCE & CODE SECURITY — PART 13
              </div>
              <h1
                style={{
                  margin: 0,
                  color: "#ffffff",
                  fontSize: "36px",
                  fontWeight: 800,
                  fontFamily: "Inter, sans-serif",
                  letterSpacing: "-0.02em",
                }}
              >
                System Architecture & Non-Blocking Firmware
              </h1>
            </div>
            <div
              style={{
                backgroundColor: "rgba(16, 185, 129, 0.15)",
                border: "1px solid rgba(16, 185, 129, 0.4)",
                color: "#10b981",
                padding: "6px 14px",
                borderRadius: "8px",
                fontSize: "13px",
                fontWeight: 700,
              }}
            >
              🟢 Non-Blocking Edge Loop
            </div>
          </div>

          {/* Dual Panel: Firmware Code Snippet + Simulated Serial Monitor Output */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1.1fr 0.9fr",
              gap: "24px",
              flex: 1,
              marginTop: "20px",
              marginBottom: "20px",
            }}
          >
            {/* Left Panel: C++ ESP32 Firmware Snippet with Synchronized Audio Highlighting */}
            <div
              style={{
                backgroundColor: "#090d16",
                borderRadius: "16px",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                padding: "20px",
                display: "flex",
                flexDirection: "column",
                overflow: "hidden",
                boxShadow: "inset 0 0 20px rgba(0,0,0,0.5)",
              }}
            >
              <div
                style={{
                  fontSize: "12px",
                  fontWeight: 700,
                  color: "#64748b",
                  textTransform: "uppercase",
                  letterSpacing: "1px",
                  marginBottom: "12px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <span style={{ color: "#38bdf8" }}>📄 SentinelSleep_Firmware.ino</span>
                  <span>•</span>
                  <span style={{ color: "#a855f7" }}>#include "secrets.h"</span>
                </div>
                <span style={{ color: "#e2e8f0", fontSize: "11px" }}>AUDIO-SYNCED HIGHLIGHT</span>
              </div>

              {/* Synchronized Code Blocks */}
              <div
                style={{
                  fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
                  fontSize: "13.5px",
                  lineHeight: "1.6",
                  display: "flex",
                  flexDirection: "column",
                  gap: "10px",
                }}
              >
                {/* Block 1: Secrets Isolation */}
                <div
                  style={{
                    padding: "8px 12px",
                    borderRadius: "8px",
                    backgroundColor:
                      activeHighlightStep === "secrets"
                        ? "rgba(168, 85, 247, 0.25)"
                        : "transparent",
                    borderLeft:
                      activeHighlightStep === "secrets"
                        ? "4px solid #a855f7"
                        : "4px solid transparent",
                    boxShadow:
                      activeHighlightStep === "secrets"
                        ? "0 0 16px rgba(168, 85, 247, 0.4)"
                        : "none",
                    transition: "all 0.3s ease-in-out",
                  }}
                >
                  <div style={{ color: "#a855f7", fontWeight: 700 }}>// 1. Secrets Isolation (.gitignore)</div>
                  <div style={{ color: "#f472b6" }}>#include "secrets.h" <span style={{ color: "#94a3b8" }}>// BLYNK_AUTH_TOKEN private</span></div>
                </div>

                {/* Block 2: Enum & BlynkTimer Decoupling */}
                <div
                  style={{
                    padding: "8px 12px",
                    borderRadius: "8px",
                    backgroundColor:
                      activeHighlightStep === "reconnect"
                        ? "rgba(56, 189, 248, 0.25)"
                        : "transparent",
                    borderLeft:
                      activeHighlightStep === "reconnect"
                        ? "4px solid #38bdf8"
                        : "4px solid transparent",
                    boxShadow:
                      activeHighlightStep === "reconnect"
                        ? "0 0 16px rgba(56, 189, 248, 0.4)"
                        : "none",
                    transition: "all 0.3s ease-in-out",
                  }}
                >
                  <div style={{ color: "#38bdf8", fontWeight: 700 }}>// 2. Non-Blocking BlynkTimer Loop</div>
                  <div style={{ color: "#38bdf8" }}>enum Mode &#123; AUTO, SLEEP, STUDY, AWAY &#125;;</div>
                  <div style={{ color: "#38bdf8" }}>BlynkTimer timer; <span style={{ color: "#94a3b8" }}>// Decouples WiFi from local sensor loop</span></div>
                </div>

                {/* Block 3: Gas Safety Priority Override Branch */}
                <div
                  style={{
                    padding: "8px 12px",
                    borderRadius: "8px",
                    backgroundColor:
                      activeHighlightStep === "local_loop"
                        ? "rgba(239, 68, 68, 0.25)"
                        : "transparent",
                    borderLeft:
                      activeHighlightStep === "local_loop"
                        ? "4px solid #ef4444"
                        : "4px solid transparent",
                    boxShadow:
                      activeHighlightStep === "local_loop"
                        ? "0 0 16px rgba(239, 68, 68, 0.4)"
                        : "none",
                    transition: "all 0.3s ease-in-out",
                  }}
                >
                  <div style={{ color: "#ef4444", fontWeight: 700 }}>// 3. Highest Priority Gas Safety Loop</div>
                  <div style={{ color: "#f8fafc" }}>void processSensors() &#123;</div>
                  <div style={{ color: "#f8fafc", paddingLeft: "16px" }}>
                    if (gasAlertActive) &#123; <span style={{ color: "#ef4444", fontWeight: 700 }}>triggerGasAlert(); return;</span> &#125;
                  </div>
                  <div style={{ color: "#f8fafc" }}>&#125;</div>
                </div>
              </div>
            </div>

            {/* Right Panel: Simulated ESP32 Serial Monitor Terminal */}
            <div
              style={{
                backgroundColor: "#020617",
                borderRadius: "16px",
                border: "1px solid rgba(59, 130, 246, 0.3)",
                padding: "20px",
                display: "flex",
                flexDirection: "column",
                boxShadow: "0 8px 24px rgba(0, 0, 0, 0.6)",
              }}
            >
              <div
                style={{
                  fontSize: "12px",
                  fontWeight: 700,
                  color: "#10b981",
                  textTransform: "uppercase",
                  letterSpacing: "1px",
                  marginBottom: "12px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                <span>📟 Serial Monitor (115200 Baud)</span>
                <span style={{ color: "#f59e0b" }}>Simulated Connection Interruption</span>
              </div>

              <div
                style={{
                  flex: 1,
                  color: "#10b981",
                  fontSize: "13px",
                  lineHeight: "1.6",
                  fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
                  backgroundColor: "#090d16",
                  padding: "16px",
                  borderRadius: "12px",
                  border: "1px solid rgba(16, 185, 129, 0.2)",
                  overflow: "hidden",
                }}
              >
                <div style={{ color: "#38bdf8" }}>[WiFi] Connecting to SSID... Connected! IP: 192.168.1.105</div>
                <div style={{ color: "#a7f3d0" }}>[Blynk] Authenticated via private secrets.h token.</div>
                <div style={{ color: "#ef4444", fontWeight: 700 }}>[WARN] Wi-Fi Connection Lost! Interruption simulated.</div>
                <div style={{ color: "#f59e0b" }}>[EDGE] Local sensor loop active! Gas safety monitoring 100% running.</div>
                <div style={{ color: "#38bdf8" }}>[WiFi] Auto-reconnecting... Reconnected successfully!</div>
                <div style={{ color: "#10b981", fontWeight: 700 }}>[Blynk] Telemetry synchronized with Blynk Cloud.</div>
              </div>
            </div>
          </div>

          {/* Key Security Cards */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: "16px",
            }}
          >
            <div
              style={{
                backgroundColor:
                  activeHighlightStep === "local_loop" ? "rgba(239, 68, 68, 0.2)" : "rgba(30, 41, 59, 0.5)",
                padding: "12px 16px",
                borderRadius: "12px",
                border:
                  activeHighlightStep === "local_loop"
                    ? "1px solid rgba(239, 68, 68, 0.6)"
                    : "1px solid rgba(255, 255, 255, 0.08)",
                display: "flex",
                alignItems: "center",
                gap: "12px",
                transition: "all 0.3s ease-in-out",
              }}
            >
              <span style={{ fontSize: "20px" }}>🔥</span>
              <div>
                <div style={{ color: "#f8fafc", fontSize: "14px", fontWeight: 700 }}>Gas Priority Branch</div>
                <div style={{ color: "#94a3b8", fontSize: "12px" }}>Local override runs offline</div>
              </div>
            </div>

            <div
              style={{
                backgroundColor:
                  activeHighlightStep === "reconnect" ? "rgba(56, 189, 248, 0.2)" : "rgba(30, 41, 59, 0.5)",
                padding: "12px 16px",
                borderRadius: "12px",
                border:
                  activeHighlightStep === "reconnect"
                    ? "1px solid rgba(56, 189, 248, 0.6)"
                    : "1px solid rgba(255, 255, 255, 0.08)",
                display: "flex",
                alignItems: "center",
                gap: "12px",
                transition: "all 0.3s ease-in-out",
              }}
            >
              <span style={{ fontSize: "20px" }}>⚡</span>
              <div>
                <div style={{ color: "#f8fafc", fontSize: "14px", fontWeight: 700 }}>BlynkTimer Loop</div>
                <div style={{ color: "#94a3b8", fontSize: "12px" }}>Non-blocking hardware processing</div>
              </div>
            </div>

            <div
              style={{
                backgroundColor:
                  activeHighlightStep === "secrets" ? "rgba(168, 85, 247, 0.2)" : "rgba(30, 41, 59, 0.5)",
                padding: "12px 16px",
                borderRadius: "12px",
                border:
                  activeHighlightStep === "secrets"
                    ? "1px solid rgba(168, 85, 247, 0.6)"
                    : "1px solid rgba(255, 255, 255, 0.08)",
                display: "flex",
                alignItems: "center",
                gap: "12px",
                transition: "all 0.3s ease-in-out",
              }}
            >
              <span style={{ fontSize: "20px" }}>🛡️</span>
              <div>
                <div style={{ color: "#f8fafc", fontSize: "14px", fontWeight: 700 }}>Secrets Isolation</div>
                <div style={{ color: "#94a3b8", fontSize: "12px" }}>Token stored in private secrets.h</div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Technical Slide Viewport for Core Concept Sections */
        <div
          style={{
            width: "100%",
            height: "100%",
            padding: "48px 64px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            background: "radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.95) 100%)",
          }}
        >
          {/* Slide Header */}
          <div>
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "6px 16px",
                borderRadius: "20px",
                backgroundColor: isExplain ? "rgba(99, 102, 241, 0.15)" : "rgba(59, 130, 246, 0.15)",
                border: isExplain ? "1px solid rgba(129, 140, 248, 0.4)" : "1px solid rgba(59, 130, 246, 0.4)",
                color: isExplain ? "#a5b4fc" : "#60a5fa",
                fontSize: "13px",
                fontWeight: 700,
                letterSpacing: "1px",
                textTransform: "uppercase",
                marginBottom: "16px",
              }}
            >
              SYSTEM MODULE — PART {section.sectionNumber} OF 15
            </div>

            <h1
              style={{
                margin: 0,
                color: "#ffffff",
                fontSize: "44px",
                fontWeight: 800,
                fontFamily: "Inter, sans-serif",
                letterSpacing: "-0.02em",
                lineHeight: "1.2",
              }}
            >
              {section.title}
            </h1>
          </div>

          {/* Key Bullet Highlights Container */}
          {section.keyPoints && section.keyPoints.length > 0 && (
            <div
              style={{
                display: "grid",
                gridTemplateColumns: hasPip ? "1fr" : "1fr 1fr",
                gap: "20px",
                marginTop: "24px",
              }}
            >
              {section.keyPoints.map((point, idx) => {
                const bulletEntrance = spring({
                  frame: Math.max(0, frame - 10 - idx * 4),
                  fps,
                  config: { damping: 16 },
                });

                return (
                  <div
                    key={idx}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: "16px",
                      padding: "16px 20px",
                      borderRadius: "16px",
                      backgroundColor: "rgba(30, 41, 59, 0.6)",
                      border: "1px solid rgba(255, 255, 255, 0.08)",
                      transform: `translateY(${interpolate(bulletEntrance, [0, 1], [30, 0])}px)`,
                      opacity: bulletEntrance,
                    }}
                  >
                    <div
                      style={{
                        width: "12px",
                        height: "12px",
                        borderRadius: "50%",
                        backgroundColor: isExplain ? "#818cf8" : "#3b82f6",
                        marginTop: "5px",
                        flexShrink: 0,
                        boxShadow: isExplain ? "0 0 10px #818cf8" : "0 0 10px #3b82f6",
                      }}
                    />
                    <span
                      style={{
                        color: "#f8fafc",
                        fontSize: "18px",
                        fontWeight: 600,
                        lineHeight: "1.4",
                        fontFamily: "Inter, sans-serif",
                      }}
                    >
                      {point}
                    </span>
                  </div>
                );
              })}
            </div>
          )}

          {/* Footer Metadata */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              borderTop: "1px solid rgba(255, 255, 255, 0.1)",
              paddingTop: "16px",
              color: "#64748b",
              fontSize: "14px",
              fontWeight: 500,
            }}
          >
            <span>SentinelSleep IoT System Architecture</span>
            <span>ESP32 • Wokwi • Blynk Cloud</span>
          </div>
        </div>
      )}
    </div>
  );
};
