import { Composition } from "remotion";
import { Presentation } from "./Presentation";
import { FPS, TOTAL_FRAMES } from "./timeline";

export const RemotionRoot = () => (
  <Composition
    id="SentinelSleep"
    component={Presentation}
    durationInFrames={TOTAL_FRAMES}
    fps={FPS}
    width={1920}
    height={1080}
  />
);
