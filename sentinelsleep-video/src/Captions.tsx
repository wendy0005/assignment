import { useCallback, useEffect, useMemo, useState } from "react";
import { Sequence, staticFile, useCurrentFrame, useDelayRender, useVideoConfig } from "remotion";
import { createTikTokStyleCaptions } from "@remotion/captions";
import type { Caption, TikTokPage } from "@remotion/captions";

const PAGE_WINDOW_MS = 1500;
const CAPTION_FILES = Array.from({ length: 9 }, (_, index) => index + 1);

export type CaptionSets = Record<number, Caption[]>;

export const useCaptionSets = () => {
  const [captions, setCaptions] = useState<CaptionSets | null>(null);
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender("Loading word-timed captions"));

  const fetchCaptions = useCallback(async () => {
    try {
      const entries = await Promise.all(
        CAPTION_FILES.map(async (number) => {
          const response = await fetch(staticFile(`captions/${number}.json`));
          if (!response.ok) {
            throw new Error(`Could not load captions for clip ${number}`);
          }
          return [number, (await response.json()) as Caption[]] as const;
        }),
      );
      setCaptions(Object.fromEntries(entries) as CaptionSets);
      continueRender(handle);
    } catch (error) {
      cancelRender(error instanceof Error ? error : new Error(String(error)));
    }
  }, [cancelRender, continueRender, handle]);

  useEffect(() => {
    fetchCaptions();
  }, [fetchCaptions]);

  return captions;
};

const CaptionPage = ({ page }: { page: TikTokPage }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const absoluteTimeMs = page.startMs + (frame / fps) * 1000;

  return (
    <div
      style={{
        position: "absolute",
        left: 82,
        bottom: 92,
        width: 1260,
        display: "flex",
        justifyContent: "center",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          maxWidth: 1160,
          borderRadius: 18,
          padding: "14px 24px 16px",
          background: "rgba(7, 18, 35, 0.88)",
          border: "1px solid rgba(125, 211, 252, 0.28)",
          boxShadow: "0 14px 42px rgba(0, 0, 0, 0.34)",
          textAlign: "center",
          fontSize: 50,
          fontWeight: 700,
          lineHeight: 1.16,
          letterSpacing: -0.8,
          color: "white",
          whiteSpace: "pre-wrap",
        }}
      >
        {page.tokens.map((token, index) => {
          const isActive =
            token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;
          return (
            <span
              key={`${token.fromMs}-${index}`}
              style={{ color: isActive ? "#67e8f9" : "#f8fafc" }}
            >
              {token.text}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export const SegmentCaptions = ({
  captions,
  sourceStartSec,
  sourceEndSec,
}: {
  captions: Caption[];
  sourceStartSec: number;
  sourceEndSec: number;
}) => {
  const { fps } = useVideoConfig();
  const sourceStartMs = sourceStartSec * 1000;
  const sourceEndMs = sourceEndSec * 1000;

  const adjusted = useMemo(
    () =>
      captions
        .filter(
          (caption) =>
            caption.endMs > sourceStartMs && caption.startMs < sourceEndMs,
        )
        .map((caption) => ({
          ...caption,
          startMs: Math.max(0, caption.startMs - sourceStartMs),
          endMs: Math.min(sourceEndMs, caption.endMs) - sourceStartMs,
          timestampMs:
            caption.timestampMs === null
              ? null
              : Math.max(0, caption.timestampMs - sourceStartMs),
        })),
    [captions, sourceEndMs, sourceStartMs],
  );

  const pages = useMemo(
    () =>
      createTikTokStyleCaptions({
        captions: adjusted,
        combineTokensWithinMilliseconds: PAGE_WINDOW_MS,
      }).pages,
    [adjusted],
  );

  return (
    <>
      {pages.map((page, index) => {
        const startFrame = Math.round((page.startMs / 1000) * fps);
        const lastTokenEnd = Math.max(...page.tokens.map((token) => token.toMs));
        const nextPageStart = pages[index + 1]?.startMs ?? Number.POSITIVE_INFINITY;
        const endMs = Math.min(lastTokenEnd + 180, nextPageStart);
        const endFrame = Math.max(
          startFrame + 1,
          Math.round((endMs / 1000) * fps),
        );

        return (
          <Sequence
            key={`${page.startMs}-${index}`}
            from={startFrame}
            durationInFrames={endFrame - startFrame}
          >
            <CaptionPage page={page} />
          </Sequence>
        );
      })}
    </>
  );
};
