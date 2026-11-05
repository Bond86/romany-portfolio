# Romany Samir — Interactive Portfolio

Live website: https://bond86.github.io/romany-portfolio/

A responsive React + TypeScript + Vite portfolio with a lazy-loaded Three.js hero, seven project case studies, thirteen verified YouTube demonstrations, searchable work and skills, career timeline, online CV, two generated PDFs, light/dark themes and static route metadata.

## Run

Node 24 recommended.

```sh
npm ci
npm run dev
```

```sh
npm run lint
npm test
npm run build
npm run preview -- --port 5189
```

The production website is in `dist/`. Do not open `index.html` directly from the filesystem; use the local server or static hosting. There is no application backend, message submission service or runtime API key.

## Content editing

- `src/data/profile.json`: canonical profile, contact, career, skills, education, certifications and languages. Website and both generated PDFs read this file.
- `src/data/projects.json`: public case studies. Add a record following the existing shape. Categories, search, technology filters, routes, related projects and sitemap update automatically.
- `src/data/videos.json`: curated verified videos and project mappings. IDs must be real; dates are upload dates.
- `src/data/behance.json`: supplied Behance references. Replace editorial cards only after approved original assets are available.
- Private and unverified drafts are excluded from this public repository.
- `public/media/projects/`: actual local thumbnails and future approved project assets.

Preserve the distinction between a concept visual and a real project screenshot. Do not publish confidential or unreleased details. Unverified and private projects are not included in this public repository.

## Regenerate PDFs

Python with `reportlab` and `pypdf` is required:

```sh
python scripts/generate-resumes.py
```

This writes `public/resumes/Romany_Samir_ATS.pdf` and `public/resumes/Romany_Samir_Professional.pdf`. Both have selectable text. Original supplied PDFs remain unchanged under `docs/resumes/`. Render and visually inspect regenerated PDFs before publishing.

## GitHub Pages

1. Push this directory as the repository root on branch `main`.
2. In repository Settings → Pages, choose **GitHub Actions**.
3. Set repository variables:
   - `BASE_PATH`: `/romany-portfolio/` for a project repository, or `/` for an account site/custom domain.
   - `SITE_URL`: origin only, e.g. `https://yourname.github.io` or `https://romanysamir.com`, without the repository path or trailing slash.
4. Run the included Pages workflow or push to `main`.

The postbuild script generates every known route as a static directory with page-specific titles, description, canonical, Open Graph, structured data, sitemap, robots.txt and `.nojekyll`. The 404 fallback supports client navigation; unsupported unknown paths show a real not-found view. No DNS is changed and no CNAME is installed automatically. Configure a custom domain only after choosing the hosting destination.

PowerShell example for a project-path build:

```powershell
$env:BASE_PATH='/romany-portfolio/'
$env:SITE_URL='https://yourname.github.io'
npm run build
```

## Media updates

`npm run sync:videos` uses the official YouTube Data API only when `YOUTUBE_API_KEY` is provided in the environment. Without a key it retains the working committed manifest. Failures leave the existing file intact. Only approved mapped videos are updated; new uploads need editorial review. Do not prefix the key with `VITE_` or put it in frontend files.

The manual **Refresh approved video metadata** workflow reads a GitHub Actions secret named `YOUTUBE_API_KEY` and commits manifest changes. A workflow-token push does not automatically trigger a second workflow: run the Pages workflow after reviewing a refresh. No scheduled automatic publication is enabled. Behance updates are manual; no unsupported API or runtime scraper is used.

## Design and accessibility

Graphite backgrounds, restrained cyan accents, Manrope/DM Sans typography and a procedural modular world. No stock screenshots or fabricated project media. WebGL has a CSS fallback; motion respects reduced-motion preferences and pauses offscreen. Video players are created only after activation, using YouTube’s privacy-enhanced domain. Native dialogs support focus containment and Escape. Contact creates a mail draft rather than pretending to submit a form.

Validation: strict TypeScript, ESLint, content/media/PDF tests, static-route verification and browser checks across mobile, tablet and desktop. No Lighthouse score is claimed.

