# 60-second portfolio showreel

Output: `public/media/showreel/romany-samir-showreel.mp4` — exactly 60.00 seconds, 1,800 frames at 30 fps, 1280 × 720 H.264 with AAC stereo audio, fast-start metadata, approximately 8.5 MiB.

The edit uses excerpts from all 18 verified portfolio demonstrations: five KSA/Adobe films and thirteen YouTube educational demonstrations. Pushcraft is represented through the owner-approved gameplay screenshot, level-editor screenshot and project key art, with restrained motion. These are explicitly labeled as still images/key art rather than invented gameplay footage.

The instrumental pulse was synthesized specifically for this edit with code; no third-party music or original source-video audio is included. The opening and closing cards, lower-thirds and poster use the portfolio’s forest-green/paper/yellow identity. The detailed frame-by-frame edit list is in `showreel-edit.json`.

## Placement

The reel is the first playable video on the homepage and the featured video on the Videos page. It opens a native HTML video player with controls, audio and download access. It does not download and autoplay the full file on initial page load; the lightweight poster appears first. Original project films remain available in the gallery.

## Rebuild

Install `imageio-ffmpeg`, `yt-dlp`, `numpy` and `Pillow` in the Python environment, or use the ignored `tmp/video-tools` package directory. Source videos belong in `tmp/showreel/source/<verified-video-id>.mp4` and are excluded from Git. Adobe source clips come from the public original player or owner-provided downloads; signed delivery URLs are never committed.

1. `python scripts/fetch-showreel-sources.py` retrieves the verified public YouTube portfolio videos.
2. `python scripts/build-showreel.py --inspect` makes contact sheets for selecting source moments.
3. `python scripts/build-showreel.py` renders the edit, synthesizes the original score, creates the poster and validates duration and full decode.

The supplied fetch helper may download the official yt-dlp JavaScript component from its GitHub distribution when needed. It never reads browser cookies or private accounts. The edit was visually reviewed through source contact sheets and rendered montage samples. FFmpeg decoded the complete final file successfully. The automated MP4-header check independently verifies its 60-second movie duration and all 18 source mappings.

Browser QA confirmed native playback advancing with readyState 4, duration 60 seconds and no media error. The homepage and Videos-page featured buttons both open this file. Escape and close controls stop playback. At a 320-pixel viewport, the homepage has no horizontal overflow and its first playable video is the showreel. The poster is used before activation, avoiding an 8.5 MiB automatic download on arrival.
