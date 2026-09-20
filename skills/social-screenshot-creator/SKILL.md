---
name: social-screenshot-creator
description: Generate pixel-perfect 2x Retina screenshots of social media posts for LinkedIn, Threads, and X (Twitter). Produces post cards and comments for all 3 platforms in one command. Trigger when user says "make a screenshot post", "generate fake social screenshot", "create post preview", or wants to visualize a post as a realistic social media capture.
---

# Social Screenshot Creator

Generates realistic, high-resolution (2x Retina) screenshots of social media posts for **LinkedIn** (light theme), **Threads** (dark theme), and **X / Twitter** (black theme).

All 3 platforms are rendered simultaneously via Playwright from a single post text input, with optional comment thread captures.

---

## ⚡ Quickstart

### Prerequisites
```bash
pip install playwright pillow
playwright install chromium
```

### Basic Generation
```bash
python3 scripts/generate_screenshot.py \
  --text "Your post content goes here. Paragraph breaks are preserved.\n\nKey takeaways: ..."
```

Outputs 3 high-res images in `./screenshots/YYYY-MM-DD_slug/`:
- `linkedin_post.png` (LinkedIn Light card)
- `threads_post.png` (Threads Dark card)
- `x_post.png` (X.com Black card)

### With Custom Persona & Avatar
```bash
python3 scripts/generate_screenshot.py \
  --text "AI engineering is shifting from prompt-tuning to deterministic governance loops." \
  --name "Sarah Connor" \
  --handle "sarahconnor" \
  --title "Robotics & AI Lead" \
  --avatar "path/to/custom_avatar.jpg" \
  --output-dir "./output"
```

### With Attached Comment Variant
```bash
python3 scripts/generate_screenshot.py \
  --text "Main post text..." \
  --comment "First follow-up comment or link drop..."
```
This produces an additional 3 images capturing the post with its first threaded reply.

---

## 🛠️ CLI Flags & Options

| Argument | Default | Description |
|---|---|---|
| `--text` | *(Required)* | Full body text of the post. |
| `--comment` | `None` | Optional follow-up comment text. |
| `--name` | `Alex Rivers` | Author display name. |
| `--handle` | `alexrivers` | Social handle (without `@`). |
| `--title` | `AI Engineer & Systems Architect` | Author headline / bio title. |
| `--avatar` | `assets/default_avatar.png` | Path to author avatar image. |
| `--output-dir`| `./screenshots` | Destination directory. |
| `--li-time` | `1d` | Timestamp displayed on LinkedIn card. |
| `--threads-time`| `2h` | Timestamp displayed on Threads card. |
| `--x-time` | `May 1` | Timestamp displayed on X card. |

---

## 🎨 Rendering Engine

Uses headless Chromium via Playwright to snapshot semantic HTML/CSS templates at `device_scale_factor=2` for crisp Retina display on mobile feeds and blogs.
