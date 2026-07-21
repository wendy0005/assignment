# SentinelSleep presentation video

Remotion composition for the BCL1123 SentinelSleep proposal presentation.

## Preview

```bash
cd /Users/tankarhau/PycharmProjects/assignment/sentinelsleep-video
npm run dev
```

Open the local URL printed by Remotion Studio, select `SentinelSleep`, and use
the timeline or Space key to scrub and play the presentation.

## Verify and render

```bash
npm run lint
npx remotion render SentinelSleep out/SentinelSleep_Final.mp4 \
  --codec=h264 --crf=18 --audio-codec=aac
```

The completed render is written to `out/SentinelSleep_Final.mp4`.

## Regenerate subtitles

Captions are generated from the nine source recordings with `faster-whisper`,
then corrected against the approved presentation script while preserving the
measured word timestamps.

```bash
../.venv/bin/python3 create_captions.py
```

The generated Remotion `Caption[]` files are stored under `public/captions/`.
The source recordings remain unchanged.
