---
name: social-screenshot-creator
description: Generate realistic fake screenshots of social media posts for LinkedIn, Threads, and X.com. Produces all 3 platforms at once (+ optional comment variants), saved into a dated folder. Trigger when user says "make a screenshot post", "create fake screenshot", "сделай скрин поста", "сделай как будто скрин из соцсети", "сделай пост как в инстаграм/линкедин/threads/x", or wants to make a post image that looks like a real social media post.
---

# Social Screenshot Creator

Generates realistic-looking screenshots of your social media posts — LinkedIn (light), Threads (dark), X/Twitter (black).

All 3 platforms are generated at once in one command. 3 posts + 3 comments (if comment text provided) = up to 6 images in a single dated folder.

**Fixed identity** (do not change unless explicitly asked):
- Name: `Vitaliy Alhimovich`
- Handle: `ilovefiniki`
- Title: `AI Engineer | Reduce manual work and get more leads using AI automations`
- Avatar: `/Users/vit/PROJECTS/Shared Skills/.agents/skills/quote_image_creator/assets/avatar.jpg`
- Output base: `/Users/vit/PROJECTS/Social Media posting/screenshots/`

---

## Step 1: Get the content

Extract from the user's message:

1. **Post text** (required) — the full post body. Preserve paragraph breaks.
2. **Comment text** (optional) — if the user wants comment variants too. Ask if unclear.

If the user provides a long post with multiple paragraphs — use the full text, don't trim.

---

## Step 2: Run the script

```bash
python3 "/Users/vit/PROJECTS/Shared Skills/.agents/skills/social_screenshot_creator/scripts/generate_screenshot.py" \
  --text "POST TEXT HERE (with \n for line breaks if needed)" \
  --output-dir "/Users/vit/PROJECTS/Social Media posting/screenshots" \
  --avatar "/Users/vit/PROJECTS/Shared Skills/.agents/skills/quote_image_creator/assets/avatar.jpg"
```

**With comment:**
```bash
python3 "..." \
  --text "POST TEXT" \
  --comment "COMMENT TEXT" \
  --output-dir "/Users/vit/PROJECTS/Social Media posting/screenshots" \
  --avatar "..."
```

The script auto-creates a subfolder: `YYYY-MM-DD_first-words-of-post/`

Inside it generates:
```
linkedin_post.png
threads_post.png
x_post.png
linkedin_comment.png  ← only if --comment provided
threads_comment.png
x_comment.png
```

---

## Step 3: Show the results

Show all generated images side by side so the user can pick which one(s) to use.

---

## Optional parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--slug custom-name` | auto from text | Custom folder name slug |
| `--li-time "3mo"` | `3mo` | Time label on LinkedIn |
| `--threads-time "2h"` | `2h` | Time label on Threads |
| `--x-time "May 1"` | `May 1` | Time + date on X |
| `--name "..."` | Vitaliy Alhimovich | Override display name |
| `--handle "..."` | ilovefiniki | Override @handle |
| `--title "..."` | AI Engineer \| ... | Override bio line |

---

## Output folder naming

Always: `YYYY-MM-DD_slug/` inside the screenshots base folder.

The slug is auto-generated from the first 5 words of the post text. To use a custom slug:
```bash
--slug "my-custom-topic"
```

Result: `/Users/vit/PROJECTS/Social Media posting/screenshots/2026-08-23_my-custom-topic/`

---

## Common examples

**Post only (no comment):**
```bash
python3 "...generate_screenshot.py" \
  --text "Biohacking in an evening. Air, AI, and curiosity.

Recently bought a simple air quality sensor..." \
  --output-dir "/Users/vit/PROJECTS/Social Media posting/screenshots" \
  --avatar "...avatar.jpg" \
  --threads-time "2h" \
  --x-time "Aug 20"
```

**Post + comment:**
```bash
python3 "...generate_screenshot.py" \
  --text "POST BODY" \
  --comment "COMMENT BODY" \
  --output-dir "..." \
  --avatar "..."
```

---

## Tilted Sticker Cards on Dot-Grid Canvas (`generate_stickers.py`)

Generates stylish, casually tilted dark screenshot "stickers" on a light or dark dot-grid canvas.
**Ideal for:**
- Highlighting external opinions, contrarian arguments, or quotes from clients/skeptics.
- Contrasting two opposing viewpoints (e.g., Tech Hype vs. Engineering Reality).
- Creating higher dwell-time visuals than generic flat single-quote images.

### Built-in Fictional AI Personas Library

The skill comes with **10 pre-generated photorealistic tech avatars** and personas (`assets/personas.json` and `assets/avatars/`):
- `david_miller` (@davidmiller_dev) — Senior Backend Engineer
- `sarah_jenkins` (@sarahj_design) — Lead Product Designer
- `alex_chen` (@alexc_systems) — AI Architect & Tech Lead
- `elena_rostova` (@elena_frontend) — Frontend Engineering Lead
- `marcus_vance` (@marcus_cloud) — DevOps & Cloud Architect
- `maya_patel` (@mayapatel_pm) — Head of Product
- `liam_oconnor` (@liam_fullstack) — Fullstack Developer
- `chloe_dubois` (@chloe_vp_eng) — VP of Engineering
- `lucas_meyer` (@lucasmeyer_ml) — ML Research Engineer
- `sofia_rossi` (@sofiarossi_b2b) — B2B Marketing Director

**Zero-config auto personas:**
If no persona or avatar is provided, `generate_stickers.py` automatically picks two distinct random personas (e.g. 1 male, 1 female) and populates realistic names, handles, and photorealistic avatars!

### Mode 1: Dual Tilted Stickers (Default — Debate / Contrast)

```bash
python3 "/Users/vit/PROJECTS/Shared Skills/.agents/skills/social_screenshot_creator/scripts/generate_stickers.py" \
  --card1-text "AI code is cheap. Architectural mistakes are expensive." \
  --card2-text "Why pay \$20/month when you can build it in an evening?" \
  --output "/Users/vit/PROJECTS/Social Media posting/screenshots/YYYY-MM-DD_topic/dual_stickers.png"
```

### Mode 2: Single Tilted Card (Centrally Tilted on Dot-Grid)

```bash
python3 "/Users/vit/PROJECTS/Shared Skills/.agents/skills/social_screenshot_creator/scripts/generate_stickers.py" \
  --mode single \
  --card1-persona "alex_chen" \
  --card1-text "The most expensive decision in AI-native engineering is knowing when to stop." \
  --output "/Users/vit/PROJECTS/Social Media posting/screenshots/YYYY-MM-DD_topic/single_sticker.png"
```

### Advanced Options:
- `--mode`: `dual` (default, 2 overlapping tilted cards) or `single` (1 centered tilted card).
- `--bg-style`: `dot-grid` (default light gray dots), `dark-dot-grid` (sleek dark canvas), or `clean-light` (pure minimalist).
- `--card1-persona` / `--card2-persona`: Specific ID from `personas.json` or `random`.
- `--card1-name`, `--card1-handle`, `--card1-avatar`: Override with Vitaliy's own profile or custom data if needed.


