import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

export const ClosingSlide: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], {
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
      <div style={{ textAlign: "center", opacity }}>
        <div
          style={{
            fontSize: 56,
            fontWeight: 700,
            color: "#38bdf8",
            marginBottom: 20,
          }}
        >
          Thank You
        </div>
        <div style={{ fontSize: 24, fontWeight: 300, marginBottom: 8 }}>
          SentinelSleep
        </div>
        <div style={{ fontSize: 20, fontWeight: 300, marginBottom: 4 }}>
          Chan Jing Yi &bull; SUOL2500321
        </div>
        <div
          style={{
            fontSize: 16,
            fontWeight: 200,
            color: "#94a3b8",
            marginTop: 24,
          }}
        >
          Wokwi: wokwi.com/projects/469850121140731905
        </div>
      </div>
    </AbsoluteFill>
  );
};
