import React from "react";

interface Props {
  currentFrame: number;
  totalFrames: number;
}

export const ProgressBar: React.FC<Props> = ({ currentFrame, totalFrames }) => {
  const progressPercent = Math.min(100, Math.max(0, (currentFrame / totalFrames) * 100));

  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        width: "100%",
        height: "6px",
        backgroundColor: "rgba(255, 255, 255, 0.15)",
        zIndex: 20,
      }}
    >
      <div
        style={{
          width: `${progressPercent}%`,
          height: "100%",
          background: "linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%)",
          boxShadow: "0 0 12px rgba(59, 130, 246, 0.8)",
          transition: "width 0.1s linear",
        }}
      />
    </div>
  );
};
