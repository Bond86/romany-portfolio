# Redesign QA — 5 November 2026

## Implementation

- Light-first paper, forest green and yellow design; dark theme retained.
- New homepage leads with Romany’s name, role and an actual mobile-controlled map demonstration.
- Four main navigation links; five grouped project filters.
- Prominent Prophet’s Biography Museum section and media-backed case study.
- 18 videos total: 13 original YouTube videos and 5 verified Behance/Adobe films.
- Original KSA and Greek project covers replace editorial placeholders.
- Eight published case studies and 17 generated static routes.
- Removed the generic Three.js hero from source and production. Main application remains about 98 KB gzipped; no 134 KB gzipped WebGL scene is loaded.

## Executed checks

- TypeScript, ESLint, production build and static-route/local-asset verification.
- Automated content, publication boundary, PDF, and provider/project mapping tests.
- Browser review at desktop and mobile sizes.
- Adobe player loaded the original mobile-controlled map film with duration 54 seconds and readyState 4. Interaction started actual playback (paused=false, currentTime advancing).
- Original museum film metadata loaded with duration 143 seconds; virtual exhibition duration 39 seconds; interior walkthrough duration 31 seconds; VR exploration duration 138 seconds.
- Museum video category filter returned five films; searching “VR model” returned one.
- Player closed with Escape and the close control.
- At 320 px, all reviewed main pages and the museum/VR case studies fit without horizontal overflow after fixes. Original local posters loaded without broken-image errors.
- Mobile menu navigation, grouped museum filter (3 projects), Unity filter (5 projects), empty search and reset were checked in-browser.
- Dark/light switching was checked; no captured application console errors in the final desktop review.
- Both canonical-data PDFs were regenerated and all six rendered pages visually reviewed after the museum name and geographic-content update.
- No claim is made that every external video plays uninterrupted on every network/device.

All video titles for the untitled KSA players are explicitly editorial descriptions. No unsupported venue counts, millions-of-visitor claims or expanded learner totals have been published. See media-verification.md for source details.
