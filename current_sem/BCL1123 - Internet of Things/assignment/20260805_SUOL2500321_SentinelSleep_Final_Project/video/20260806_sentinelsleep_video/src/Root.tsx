import { Composition } from "remotion";
import "./index.css";
import { SentinelSleepVideo } from "./SentinelSleepVideo";
import { TOTAL_DURATION_IN_FRAMES } from "./sectionsData";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="SentinelSleepAvatarDemo"
        component={SentinelSleepVideo}
        durationInFrames={TOTAL_DURATION_IN_FRAMES}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          mode: "avatar",
        }}
      />

      <Composition
        id="SentinelSleepCleanDemo"
        component={SentinelSleepVideo}
        durationInFrames={TOTAL_DURATION_IN_FRAMES}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          mode: "clean",
        }}
      />
    </>
  );
};
