import { AbsoluteFill, Sequence, staticFile } from "remotion";
import { Audio, Video } from "@remotion/media";
import { SegmentCaptions, useCaptionSets } from "./Captions";
import { SectionVisual } from "./Visuals";
import {
  getClipFrames,
  getClipStartFrames,
  getSegmentFrames,
  secondsToFrames,
} from "./timeline";
import type { CaptionSets } from "./Captions";
import type { ClipSpec } from "./timeline";

const PresenterTrack = ({ clip }: { clip: ClipSpec }) => {
  let cursor = 0;
  return (
    <div
      style={{
        position: "absolute",
        left: 1432,
        top: 154,
        width: 410,
        height: 729,
        overflow: "hidden",
        borderRadius: 28,
        border: "3px solid rgba(103, 232, 249, 0.72)",
        boxShadow: "0 28px 75px rgba(0, 0, 0, 0.42)",
        background: "#071223",
      }}
    >
      {clip.segments.map((segment, index) => {
        const durationInFrames = getSegmentFrames(segment);
        const from = cursor;
        cursor += durationInFrames;
        return (
          <Sequence key={`${clip.number}-${index}`} from={from} durationInFrames={durationInFrames}>
            <Video
              src={staticFile(clip.file)}
              trimBefore={secondsToFrames(segment.startSec)}
              trimAfter={secondsToFrames(segment.endSec)}
              muted
              objectFit="cover"
              style={{ width: "100%", height: "100%" }}
            />
            <Audio
              src={staticFile(`audio/${clip.number}.m4a`)}
              trimBefore={secondsToFrames(segment.startSec)}
              trimAfter={secondsToFrames(segment.endSec)}
            />
          </Sequence>
        );
      })}
    </div>
  );
};

const ClipCaptions = ({ clip, captions }: { clip: ClipSpec; captions: CaptionSets }) => {
  let cursor = 0;
  return (
    <>
      {clip.segments.map((segment, index) => {
        const durationInFrames = getSegmentFrames(segment);
        const from = cursor;
        cursor += durationInFrames;
        return (
          <Sequence key={`${clip.number}-${index}`} from={from} durationInFrames={durationInFrames}>
            <SegmentCaptions
              captions={captions[clip.number] ?? []}
              sourceStartSec={segment.startSec}
              sourceEndSec={segment.endSec}
            />
          </Sequence>
        );
      })}
    </>
  );
};

const ClipScene = ({ clip, captions }: { clip: ClipSpec; captions: CaptionSets }) => {
  const durationInFrames = getClipFrames(clip);
  return (
    <AbsoluteFill>
      <SectionVisual clip={clip} durationInFrames={durationInFrames} />
      <PresenterTrack clip={clip} />
      <div
        style={{
          position: "absolute",
          left: 1432,
          top: 902,
          width: 416,
          textAlign: "center",
          color: "#dbeafe",
          fontSize: 23,
          fontWeight: 750,
          letterSpacing: 0.5,
        }}
      >
        CHAN JING YI · SUOL2500321
      </div>
      <ClipCaptions clip={clip} captions={captions} />
    </AbsoluteFill>
  );
};

export const Presentation = () => {
  const captions = useCaptionSets();
  if (!captions) {
    return null;
  }

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 82% 16%, rgba(14,165,233,0.18), transparent 28%), radial-gradient(circle at 9% 82%, rgba(52,211,153,0.10), transparent 30%), linear-gradient(145deg, #07111f 0%, #0b1730 56%, #101d37 100%)",
        fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, sans-serif",
      }}
    >
      <div style={{ position: "absolute", right: -180, top: -240, width: 640, height: 640, borderRadius: "50%", border: "1px solid rgba(56,189,248,0.12)" }} />
      <div style={{ position: "absolute", right: -80, top: -130, width: 420, height: 420, borderRadius: "50%", border: "1px solid rgba(103,232,249,0.10)" }} />
      {getClipStartFrames().map(({ clip, startFrame }) => (
        <Sequence key={clip.number} from={startFrame} durationInFrames={getClipFrames(clip)}>
          <ClipScene clip={clip} captions={captions} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
