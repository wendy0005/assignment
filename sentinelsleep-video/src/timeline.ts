export const FPS = 30;

export type SourceSegment = {
  startSec: number;
  endSec: number;
};

export type ClipSpec = {
  number: number;
  file: string;
  section: string;
  eyebrow: string;
  segments: SourceSegment[];
};

export const CLIPS: ClipSpec[] = [
  {
    number: 1,
    file: "1.mp4",
    section: "SentinelSleep",
    eyebrow: "INTRODUCTION",
    segments: [{ startSec: 0, endSec: 22.9 }],
  },
  {
    number: 2,
    file: "2.mp4",
    section: "The bedroom problem",
    eyebrow: "TARGET ENVIRONMENT",
    segments: [{ startSec: 0, endSec: 32.625 }],
  },
  {
    number: 3,
    file: "3.mp4",
    section: "Proposed solution",
    eyebrow: "HARDWARE",
    segments: [{ startSec: 4.89, endSec: 57.45 }],
  },
  {
    number: 4,
    file: "4.mp4",
    section: "Priority-based control",
    eyebrow: "CONTROL LOGIC",
    segments: [
      { startSec: 0, endSec: 24.847 },
      { startSec: 31.05, endSec: 61.98 },
      { startSec: 68.5, endSec: 91.806 },
      { startSec: 100.508, endSec: 124.17 },
      { startSec: 129.25, endSec: 151.23 },
    ],
  },
  {
    number: 5,
    file: "5.mp4",
    section: "Four connected layers",
    eyebrow: "IOT ARCHITECTURE",
    segments: [
      { startSec: 0, endSec: 15.429 },
      { startSec: 16.679, endSec: 71.295 },
    ],
  },
  {
    number: 6,
    file: "6.mp4",
    section: "Explainable dashboard",
    eyebrow: "APPLICATION",
    segments: [{ startSec: 0, endSec: 31.7 }],
  },
  {
    number: 7,
    file: "7.mp4",
    section: "Why SentinelSleep is different",
    eyebrow: "UNIQUENESS",
    segments: [{ startSec: 0, endSec: 49.12 }],
  },
  {
    number: 8,
    file: "8.mp4",
    section: "Prototype and limitations",
    eyebrow: "WOKWI DEMONSTRATION",
    segments: [{ startSec: 0, endSec: 65.733 }],
  },
  {
    number: 9,
    file: "9.mp4",
    section: "A practical foundation",
    eyebrow: "CONCLUSION",
    segments: [{ startSec: 0, endSec: 22.9 }],
  },
];

export const secondsToFrames = (seconds: number) => Math.round(seconds * FPS);

export const getSegmentFrames = (segment: SourceSegment) =>
  secondsToFrames(segment.endSec - segment.startSec);

export const getClipFrames = (clip: ClipSpec) =>
  clip.segments.reduce((sum, segment) => sum + getSegmentFrames(segment), 0);

export const TOTAL_FRAMES = CLIPS.reduce(
  (sum, clip) => sum + getClipFrames(clip),
  0,
);

export const getClipStartFrames = () => {
  let cursor = 0;
  return CLIPS.map((clip) => {
    const startFrame = cursor;
    cursor += getClipFrames(clip);
    return { clip, startFrame };
  });
};
