import type { ReactNode } from "react";
import { Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import type { ClipSpec } from "./timeline";

const COLORS = {
  navy: "#0b1730",
  panel: "rgba(17, 35, 62, 0.90)",
  cyan: "#38bdf8",
  aqua: "#67e8f9",
  green: "#34d399",
  amber: "#fbbf24",
  red: "#fb7185",
  white: "#f8fafc",
  muted: "#a9bad0",
};

const Panel = ({ children }: { children: ReactNode }) => (
  <div
    style={{
      width: "100%",
      height: "100%",
      borderRadius: 30,
      padding: 34,
      boxSizing: "border-box",
      background: COLORS.panel,
      border: "1px solid rgba(125, 211, 252, 0.20)",
      boxShadow: "0 26px 70px rgba(0, 0, 0, 0.28)",
      overflow: "hidden",
    }}
  >
    {children}
  </div>
);

const Badge = ({ children, color = COLORS.cyan }: { children: ReactNode; color?: string }) => (
  <div
    style={{
      borderRadius: 999,
      padding: "12px 20px",
      color,
      background: `${color}18`,
      border: `1px solid ${color}55`,
      fontSize: 28,
      fontWeight: 700,
      lineHeight: 1,
      whiteSpace: "nowrap",
    }}
  >
    {children}
  </div>
);

const Feature = ({ title, detail, color }: { title: string; detail: string; color: string }) => (
  <div
    style={{
      flex: 1,
      minHeight: 158,
      borderRadius: 22,
      padding: 24,
      background: "rgba(255,255,255,0.055)",
      borderTop: `5px solid ${color}`,
      boxSizing: "border-box",
    }}
  >
    <div style={{ fontSize: 34, fontWeight: 800, color: COLORS.white }}>{title}</div>
    <div style={{ marginTop: 12, fontSize: 26, lineHeight: 1.25, color: COLORS.muted }}>{detail}</div>
  </div>
);

const Intro = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <Panel>
      <div style={{ height: "100%", display: "flex", flexDirection: "column", justifyContent: "center", opacity }}>
        <div style={{ fontSize: 108, fontWeight: 900, lineHeight: 0.95, letterSpacing: -4, color: COLORS.white }}>
          Sentinel<span style={{ color: COLORS.cyan }}>Sleep</span>
        </div>
        <div style={{ marginTop: 24, maxWidth: 1050, fontSize: 45, lineHeight: 1.18, fontWeight: 650, color: "#dce8f7" }}>
          An occupancy-aware smart bedroom for comfort, energy and safety
        </div>
        <div style={{ display: "flex", gap: 18, marginTop: 46 }}>
          <Feature title="Energy" detail="Avoid unnecessary light and fan operation" color={COLORS.amber} />
          <Feature title="Comfort" detail="Respond to occupancy and room conditions" color={COLORS.cyan} />
          <Feature title="Safety" detail="Prioritise local and remote warnings" color={COLORS.red} />
        </div>
        <div style={{ marginTop: 30, fontSize: 28, color: COLORS.muted }}>
          BCL1123 · Internet of Things · Proposal Report &amp; Video
        </div>
      </div>
    </Panel>
  );
};

const Environment = ({ durationInFrames }: { durationInFrames: number }) => {
  const frame = useCurrentFrame();
  const swap = durationInFrames * 0.54;
  const roomOpacity = interpolate(frame, [swap - 12, swap + 12], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <Panel>
      <div style={{ position: "relative", width: "100%", height: "100%", borderRadius: 22, overflow: "hidden" }}>
        <Img src={staticFile("visuals/switch_panel.jpeg")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        <Img src={staticFile("visuals/room.jpeg")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: roomOpacity }} />
        <div style={{ position: "absolute", left: 28, top: 26, padding: "14px 20px", borderRadius: 14, background: "rgba(7,18,35,0.84)", fontSize: 31, fontWeight: 750, color: COLORS.white }}>
          {frame < swap ? "Bedroom: sleeping, studying and resting" : "Current controls: manual and disconnected"}
        </div>
        <div style={{ position: "absolute", right: 28, top: 26 }}>
          <Badge color={frame < swap ? COLORS.green : COLORS.amber}>{frame < swap ? "TARGET AREA" : "CONTROL POINT"}</Badge>
        </div>
      </div>
    </Panel>
  );
};

const Hardware = () => (
  <Panel>
    <div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <div style={{ fontSize: 34, fontWeight: 800, color: COLORS.white }}>Wokwi-supported components</div>
        <Badge>ESP32 EDGE CONTROLLER</Badge>
      </div>
      <div style={{ flex: 1, borderRadius: 20, overflow: "hidden", background: "white" }}>
        <Img src={staticFile("visuals/hardware.png")} style={{ width: "100%", height: "100%", objectFit: "contain" }} />
      </div>
      <div style={{ display: "flex", gap: 14, marginTop: 18 }}>
        <Badge color={COLORS.green}>SENSE</Badge>
        <Badge color={COLORS.cyan}>DECIDE</Badge>
        <Badge color={COLORS.amber}>ACT</Badge>
        <Badge color={COLORS.red}>ALERT</Badge>
      </div>
    </div>
  </Panel>
);

const ControlFlow = ({ durationInFrames }: { durationInFrames: number }) => {
  const frame = useCurrentFrame();
  const phases = ["Validate", "Safety first", "Lighting", "Fan", "Publish"];
  const active = Math.min(phases.length - 1, Math.floor((frame / durationInFrames) * phases.length));
  return (
    <Panel>
      <div style={{ height: "100%", display: "flex", flexDirection: "column", gap: 20 }}>
        <div style={{ display: "flex", gap: 12 }}>
          {phases.map((phase, index) => <Badge key={phase} color={index === active ? COLORS.aqua : COLORS.muted}>{index + 1}. {phase}</Badge>)}
        </div>
        <div style={{ flex: 1, borderRadius: 20, overflow: "hidden", background: "white", display: "flex", alignItems: "center" }}>
          <Img src={staticFile("visuals/control-flow.png")} style={{ width: "100%", height: "100%", objectFit: "contain", scale: 1.03 }} />
        </div>
        <div style={{ fontSize: 27, color: COLORS.muted }}>Safety overrides comfort automation · Local logic continues without the cloud</div>
      </div>
    </Panel>
  );
};

const Architecture = ({ durationInFrames }: { durationInFrames: number }) => {
  const frame = useCurrentFrame();
  const layers = ["Edge", "Connectivity", "Cloud", "Application"];
  const active = Math.min(layers.length - 1, Math.floor((frame / durationInFrames) * layers.length));
  return (
    <Panel>
      <div style={{ height: "100%", display: "flex", flexDirection: "column", gap: 20 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          {layers.map((layer, index) => <Badge key={layer} color={index === active ? COLORS.cyan : COLORS.muted}>{layer}</Badge>)}
          <div style={{ marginLeft: "auto", fontSize: 27, color: COLORS.muted }}>bidirectional data flow</div>
        </div>
        <div style={{ flex: 1, borderRadius: 20, overflow: "hidden", background: "white", display: "flex", alignItems: "center" }}>
          <Img src={staticFile("visuals/architecture.png")} style={{ width: "100%", height: "100%", objectFit: "contain" }} />
        </div>
        <div style={{ display: "flex", gap: 16 }}>
          <Feature title="Local resilience" detail="Immediate rules continue offline" color={COLORS.green} />
          <Feature title="MQTT messaging" detail="Lightweight publish and subscribe" color={COLORS.cyan} />
          <Feature title="Confirmed state" detail="Dashboard reports actual device state" color={COLORS.amber} />
        </div>
      </div>
    </Panel>
  );
};

const Dashboard = () => (
  <Panel>
    <div style={{ height: "100%", display: "flex", gap: 28, alignItems: "center" }}>
      <div style={{ height: "100%", width: 720, display: "flex", justifyContent: "center" }}>
        <Img src={staticFile("visuals/dashboard.png")} style={{ width: "100%", height: "100%", objectFit: "contain" }} />
      </div>
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 18 }}>
        <Feature title="1 · Safety first" detail="The banner answers whether the room is safe" color={COLORS.green} />
        <Feature title="2 · Live context" detail="Comfort, light and occupancy readings" color={COLORS.cyan} />
        <Feature title="3 · Explain actions" detail="Every device state includes a reason" color={COLORS.amber} />
        <Feature title="4 · Limited overrides" detail="Manual control expires automatically" color={COLORS.red} />
      </div>
    </div>
  </Panel>
);

const Comparison = () => {
  const rows = [
    ["Occupancy + comfort + warning", "Single specialised function"],
    ["Core rules continue offline", "Often ecosystem dependent"],
    ["Explains every actuator change", "Limited reason visibility"],
    ["Camera-free PIR occupancy", "Varies by product"],
  ];
  return (
    <Panel>
      <div style={{ height: "100%", display: "flex", flexDirection: "column", gap: 18 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18 }}>
          <div style={{ fontSize: 34, fontWeight: 850, color: COLORS.aqua }}>SentinelSleep</div>
          <div style={{ fontSize: 34, fontWeight: 850, color: COLORS.muted }}>Typical specialist product</div>
        </div>
        {rows.map(([ours, typical]) => (
          <div key={ours} style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, flex: 1 }}>
            <div style={{ borderRadius: 20, padding: "22px 26px", background: "rgba(52,211,153,0.10)", border: "1px solid rgba(52,211,153,0.36)", fontSize: 31, fontWeight: 700, color: COLORS.white, display: "flex", alignItems: "center" }}>✓&nbsp; {ours}</div>
            <div style={{ borderRadius: 20, padding: "22px 26px", background: "rgba(255,255,255,0.045)", border: "1px solid rgba(169,186,208,0.22)", fontSize: 29, color: COLORS.muted, display: "flex", alignItems: "center" }}>{typical}</div>
          </div>
        ))}
        <div style={{ fontSize: 34, fontWeight: 800, color: COLORS.amber }}>Priority-aware sensor fusion with explainable actions</div>
      </div>
    </Panel>
  );
};

const WokwiDemo = ({ durationInFrames }: { durationInFrames: number }) => {
  const frame = useCurrentFrame();
  const alert = frame > durationInFrames * 0.46;
  return (
    <Panel>
      <div style={{ height: "100%", display: "flex", flexDirection: "column", gap: 24 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ fontSize: 36, fontWeight: 850, color: COLORS.white }}>Wokwi prototype state</div>
          <Badge color={alert ? COLORS.red : COLORS.green}>{alert ? "GAS ALERT" : "ROOM SAFE"}</Badge>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: 24, flex: 1 }}>
          <div style={{ borderRadius: 24, padding: 30, background: "#08111f", border: "1px solid rgba(125,211,252,0.20)", fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace", fontSize: 29, lineHeight: 1.7, color: "#cbd5e1" }}>
            <div style={{ color: COLORS.cyan }}>&gt; ESP32 SentinelSleep</div>
            <div>Temperature&nbsp; 29.1 °C</div>
            <div>Humidity&nbsp;&nbsp;&nbsp; 68%</div>
            <div>Light&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 42 lux</div>
            <div>Occupancy&nbsp;&nbsp; detected</div>
            <div>MQ-2 DOUT&nbsp;&nbsp; {alert ? "LOW" : "HIGH"}</div>
            <div style={{ marginTop: 18, color: alert ? COLORS.red : COLORS.green, fontWeight: 900 }}>
              {alert ? "!!! URGENT MQTT ALERT !!!" : "Normal automation active"}
            </div>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
            <Feature title={alert ? "Buzzer ON" : "Buzzer OFF"} detail={alert ? "Immediate local warning" : "No hazard threshold"} color={alert ? COLORS.red : COLORS.green} />
            <Feature title={alert ? "RGB RED" : "RGB GREEN"} detail={alert ? "Safety overrides comfort" : "Normal room state"} color={alert ? COLORS.red : COLORS.green} />
            <Feature title="MQTT telemetry" detail="Readings and state published" color={COLORS.cyan} />
          </div>
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ fontSize: 25, color: COLORS.muted }}>wokwi.com/projects/469850121140731905</div>
          <div style={{ fontSize: 25, color: COLORS.amber }}>Prototype only · does not replace a certified alarm</div>
        </div>
      </div>
    </Panel>
  );
};

const Closing = () => (
  <Panel>
    <div style={{ height: "100%", display: "flex", flexDirection: "column", justifyContent: "center" }}>
      <Badge color={COLORS.green}>CONCLUSION</Badge>
      <div style={{ marginTop: 28, fontSize: 82, lineHeight: 1.02, fontWeight: 900, letterSpacing: -3, color: COLORS.white }}>
        Comfort, energy and safety—coordinated locally.
      </div>
      <div style={{ display: "flex", gap: 18, marginTop: 42 }}>
        <Feature title="Feasible" detail="Wokwi-compatible hardware" color={COLORS.cyan} />
        <Feature title="Private" detail="No camera or microphone" color={COLORS.green} />
        <Feature title="Resilient" detail="Core rules work offline" color={COLORS.amber} />
      </div>
      <div style={{ marginTop: 36, fontSize: 36, fontWeight: 750, color: COLORS.aqua }}>Thank you</div>
      <div style={{ marginTop: 10, fontSize: 28, color: COLORS.muted }}>Chan Jing Yi · SUOL2500321</div>
    </div>
  </Panel>
);

export const SectionVisual = ({ clip, durationInFrames }: { clip: ClipSpec; durationInFrames: number }) => (
  <>
    <div style={{ position: "absolute", left: 78, top: 58, width: 1268, display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
      <div>
        <div style={{ color: COLORS.cyan, fontSize: 24, fontWeight: 850, letterSpacing: 3 }}>{clip.eyebrow}</div>
        <div style={{ color: COLORS.white, fontSize: 48, fontWeight: 850, letterSpacing: -1.2 }}>{clip.section}</div>
      </div>
      <div style={{ color: COLORS.muted, fontSize: 26, fontWeight: 700 }}>{String(clip.number).padStart(2, "0")} / 09</div>
    </div>
    <div style={{ position: "absolute", left: 72, top: 154, width: 1280, height: 790 }}>
      {clip.number === 1 && <Intro />}
      {clip.number === 2 && <Environment durationInFrames={durationInFrames} />}
      {clip.number === 3 && <Hardware />}
      {clip.number === 4 && <ControlFlow durationInFrames={durationInFrames} />}
      {clip.number === 5 && <Architecture durationInFrames={durationInFrames} />}
      {clip.number === 6 && <Dashboard />}
      {clip.number === 7 && <Comparison />}
      {clip.number === 8 && <WokwiDemo durationInFrames={durationInFrames} />}
      {clip.number === 9 && <Closing />}
    </div>
  </>
);
