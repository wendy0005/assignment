import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

const semester = "May – August 2026";

export const TitleSlide: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });
  const subtitleOpacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0f172a",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "system-ui, sans-serif",
        color: "white",
      }}
    >
      <div style={{ textAlign: "center", opacity: titleOpacity }}>
        <div
          style={{
            fontSize: 60,
            fontWeight: 700,
            marginBottom: 12,
            color: "#38bdf8",
          }}
        >
          SentinelSleep
        </div>
        <div style={{ fontSize: 28, fontWeight: 400, marginBottom: 8 }}>
          An Occupancy-Aware Smart Bedroom
        </div>
        <div style={{ fontSize: 28, fontWeight: 400, marginBottom: 40 }}>
          Comfort, Energy and Safety System
        </div>
      </div>

      <div style={{ textAlign: "center", opacity: subtitleOpacity }}>
        <div style={{ fontSize: 24, fontWeight: 300, marginBottom: 4 }}>
          BCL1123 – Internet of Things
        </div>
        <div style={{ fontSize: 24, fontWeight: 300, marginBottom: 4 }}>
          Proposal Report & Video
        </div>
        <div style={{ fontSize: 22, fontWeight: 300, marginTop: 20 }}>
          Chan Jing Yi &bull; SUOL2500321
        </div>
        <div
          style={{
            fontSize: 16,
            fontWeight: 200,
            marginTop: 8,
            color: "#94a3b8",
          }}
        >
          {semester}
        </div>
      </div>
    </AbsoluteFill>
  );
};
