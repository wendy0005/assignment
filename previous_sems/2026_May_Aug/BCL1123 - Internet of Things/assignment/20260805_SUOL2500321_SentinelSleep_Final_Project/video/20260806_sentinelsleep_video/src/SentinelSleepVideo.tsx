import React from "react";
import { Series, useCurrentFrame } from "remotion";
import { MainProjectDisplay } from "./components/MainProjectDisplay";
import { OverlayCard } from "./components/OverlayCard";
import { PresenterCard } from "./components/PresenterCard";
import { ProgressBar } from "./components/ProgressBar";
import { SectionHeader } from "./components/SectionHeader";
import { SubtitleBar } from "./components/SubtitleBar";
import { SECTIONS, TOTAL_DURATION_IN_FRAMES } from "./sectionsData";

interface Props {
  mode?: "avatar" | "clean";
}

export const SentinelSleepVideo: React.FC<Props> = () => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: "#020617",
        position: "relative",
        overflow: "hidden",
        width: "100%",
        height: "100%",
        fontFamily: "Inter, -apple-system, sans-serif",
      }}
    >
      <Series>
        {SECTIONS.map((section) => (
          <Series.Sequence
            key={section.id}
            durationInFrames={section.durationInFrames}
            style={{
              translate: "1px 0px",
            }}
          >
            <div
              style={{
                width: "100%",
                height: "100%",
                position: "relative",
                backgroundColor: "#020617",
              }}
            >
              {/* Main Project Viewport (Wokwi Schematics, Blynk Screens, System Slides) */}
              <MainProjectDisplay section={section} />

              {/* Section Badge */}
              <SectionHeader
                sectionNumber={section.sectionNumber}
                totalSections={SECTIONS.length}
                title={section.title}
              />

              {/* Synchronized Short Subtitle Bar */}
              <SubtitleBar section={section} />

              {/* Side PIP Overlay Card for Blynk Mobile Screens */}
              <OverlayCard section={section} />

              {/* Vertical Presenter Video Card in Bottom-Right Corner */}
              <PresenterCard videoFile={section.videoFile} />
            </div>
          </Series.Sequence>
        ))}
      </Series>
      <ProgressBar
        currentFrame={frame}
        totalFrames={TOTAL_DURATION_IN_FRAMES}
      />
    </div>
  );
};
