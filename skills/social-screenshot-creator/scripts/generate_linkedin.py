#!/usr/bin/env python3
"""
LinkedIn Screenshot Generator v3.0
Uses HTML + Playwright to produce pixel-perfect LinkedIn post/comment screenshots.

Real LinkedIn specs extracted from live DOM:
  - Font:        system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial
  - Feed bg:     #F4F2EE
  - Card bg:     #FFFFFF
  - Card border: none (shadow instead: 0 0 0 1px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.08))
  - Author name: 20px / 600 / rgba(0,0,0,0.9) / line-height 25px
  - Post text:   16px / 400 / rgba(0,0,0,0.9) / line-height 28px
  - Meta text:   14px / 400 / rgba(0,0,0,0.6) / line-height 17.5px
  - Action icon: 16x16 SVG, currentColor = rgba(0,0,0,0.6)
  - Primary blue: #0A66C2
  - Card width:  ~552px (feed col) — we render at 560px for mobile crop

Usage:
  python3 generate_linkedin.py \
    --text "Post text here" \
    --output "/path/to/output.png" \
    --avatar "/path/to/avatar.jpg" \
    [--comment]          # render as comment card
    [--name "Name"]
    [--title "Title"]
    [--time "3mo"]
"""

import argparse
import base64
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# ── Real LinkedIn SVG icons (extracted from live DOM) ─────────────────────────

SVG_LIKE = '''<svg xmlns="http://www.w3.org/2000/svg" id="thumbs-up-outline-small" fill="currentColor"
     aria-hidden="true" data-supported-dps="16x16" viewBox="0 0 16 16" width="16" height="16">
  <path d="m12.91 7-2.25-2.57a8.2 8.2 0 0 1-1.5-2.55L9 1.37A2.08 2.08 0 0 0 7 0a2.08 2.08 0 0 0-2.06 2.08v1.17a5.8 5.8 0 0 0 .31 1.89l.28.86H2.38A1.47 1.47 0 0 0 1 7.47a1.45 1.45 0 0 0 .64 1.21 1.48 1.48 0 0 0-.37 2.06 1.54 1.54 0 0 0 .62.51h.05a1.6 1.6 0 0 0-.19.71A1.47 1.47 0 0 0 3 13.42v.1A1.46 1.46 0 0 0 4.4 15h4.83a5.6 5.6 0 0 0 2.48-.58l1-.42H14V7zM12 12.11l-1.19.52a3.6 3.6 0 0 1-1.58.37H5.1a.55.55 0 0 1-.53-.4l-.14-.48-.49-.21a.56.56 0 0 1-.34-.6l.09-.56-.42-.42a.56.56 0 0 1-.09-.68L3.55 9l-.4-.61A.28.28 0 0 1 3.3 8h5L7.14 4.51a4.2 4.2 0 0 1-.2-1.26V2.08A.09.09 0 0 1 7 2a.1.1 0 0 1 .08 0l.18.51a10 10 0 0 0 1.9 3.24l2.84 3z"/>
</svg>'''

SVG_COMMENT = '''<svg xmlns="http://www.w3.org/2000/svg" id="comment-small" fill="currentColor"
     aria-hidden="true" data-supported-dps="16x16" viewBox="0 0 16 16" width="16" height="16">
  <path d="M5 8h5v1H5zm11-.5v.08a6 6 0 0 1-2.75 5L8 16v-3H5.5A5.51 5.51 0 0 1 0 7.5 5.62 5.62 0 0 1 5.74 2h4.76A5.5 5.5 0 0 1 16 7.5m-2 0A3.5 3.5 0 0 0 10.5 4H5.74A3.62 3.62 0 0 0 2 7.5 3.53 3.53 0 0 0 5.5 11H10v1.33l2.17-1.39A4 4 0 0 0 14 7.58zM5 7h6V6H5z"/>
</svg>'''

SVG_REPOST = '''<svg xmlns="http://www.w3.org/2000/svg" id="repost-small" fill="currentColor"
     aria-hidden="true" data-supported-dps="16x16" viewBox="0 0 16 16" width="16" height="16">
  <path d="M4 10H2V5c0-1.66 1.34-3 3-3h3.85L7.42 0h2.44L12 3 9.86 6H7.42l1.43-2H5c-.55 0-1 .45-1 1zm8-4v5c0 .55-.45 1-1 1H7.15l1.43-2H6.14L4 13l2.14 3h2.44l-1.43-2H11c1.66 0 3-1.34 3-3V6z"/>
</svg>'''

SVG_SEND = '''<svg xmlns="http://www.w3.org/2000/svg" id="send-privately-small" fill="currentColor"
     aria-hidden="true" data-rtl="true" data-supported-dps="16x16" viewBox="0 0 16 16" width="16" height="16">
  <path d="M14 2 0 6.67l5 2.64 5.67-3.98L6.7 11l2.63 5z"/>
</svg>'''

# Verified checkmark badge (LinkedIn blue)
SVG_VERIFIED = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">
  <path fill="#0A66C2" d="M14.5 8A6.5 6.5 0 1 1 8 1.5 6.5 6.5 0 0 1 14.5 8"/>
  <path fill="#fff" d="m6.39 10.87-2.6-2.6.86-.87 1.74 1.74 3.76-3.76.86.87z"/>
</svg>'''

# Globe icon for "public" indicator
SVG_GLOBE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="14" height="14" fill="currentColor">
  <path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zM2.05 9h2.47a12.6 12.6 0 0 0 .75 3.17A5.5 5.5 0 0 1 2.05 9zm0-2a5.5 5.5 0 0 1 3.22-3.17A12.6 12.6 0 0 0 4.52 7zm4.47 5.96A11 11 0 0 1 5.54 9h4.92A11 11 0 0 1 8 14.96zM5.54 7a11 11 0 0 1 2.47-4.96A11 11 0 0 1 10.46 7zm4.74 5.17A12.6 12.6 0 0 0 11.03 9h2.92a5.5 5.5 0 0 1-3.67 3.17zM13.95 7h-2.47a12.6 12.6 0 0 0-.75-3.17A5.5 5.5 0 0 1 13.95 7z"/>
</svg>'''

# Dots menu (···)
SVG_DOTS = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 4" width="20" height="4" fill="currentColor">
  <circle cx="2" cy="2" r="2"/><circle cx="10" cy="2" r="2"/><circle cx="18" cy="2" r="2"/>
</svg>'''


import re

def avatar_to_data_uri(avatar_path: str) -> str:
    """Convert avatar image to base64 data URI for embedding in HTML."""
    with open(avatar_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(avatar_path).suffix.lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
    return f"data:image/{mime};base64,{data}"


def build_html_post(
    text: str,
    avatar_path: str,
    name: str,
    title: str,
    time_str: str,
    is_comment: bool = False,
) -> str:
    """Build the HTML string for a LinkedIn post card."""

    avatar_uri = avatar_to_data_uri(avatar_path)

    # Split by paragraph blocks (double newline) or single newlines
    blocks = re.split(r'\n\s*\n', text.strip())
    html_parts = []
    for block in blocks:
        lines = [line for line in block.split('\n')]
        # Clean lines
        rendered_block = "<br>".join(lines)
        if rendered_block.strip():
            html_parts.append(f"<p>{rendered_block}</p>")
    text_html = "\n".join(html_parts)

    badge = "You" if not is_comment else "Author"
    card_class = "card comment-card" if is_comment else "card"
    avatar_size = "40px" if is_comment else "48px"

    action_buttons = f"""
    <div class="action-bar">
      <button class="action-btn">
        <span class="action-icon">{SVG_LIKE}</span>
        <span class="action-label">Like</span>
      </button>
      <button class="action-btn">
        <span class="action-icon">{SVG_COMMENT}</span>
        <span class="action-label">Comment</span>
      </button>
      <button class="action-btn">
        <span class="action-icon">{SVG_REPOST}</span>
        <span class="action-label">Repost</span>
      </button>
      <button class="action-btn">
        <span class="action-icon">{SVG_SEND}</span>
        <span class="action-label">Send</span>
      </button>
    </div>
    """ if not is_comment else f"""
    <div class="comment-actions">
      <button class="comment-action-btn">Like</button>
      <span class="comment-dot">·</span>
      <button class="comment-action-btn">Reply</button>
      <span class="comment-dot">·</span>
      <button class="comment-action-btn">More</button>
    </div>
    """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=480">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: #F4F2EE;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    padding: 8px;
    width: 480px;
  }}

  .card {{
    background: #FFFFFF;
    border-radius: 8px;
    box-shadow: 0 0 0 1px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.05);
    overflow: hidden;
  }}

  .comment-card {{
    border-radius: 4px;
    box-shadow: none;
    border: 1px solid rgba(0,0,0,0.08);
  }}

  /* ── Header ── */
  .header {{
    display: flex;
    align-items: flex-start;
    padding: 14px 16px 0 16px;
    gap: 8px;
  }}

  .avatar {{
    width: {avatar_size};
    height: {avatar_size};
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
  }}

  .actor-info {{
    flex: 1;
    min-width: 0;
  }}

  .actor-name-row {{
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: nowrap;
  }}

  .actor-name {{
    font-size: {"15px" if is_comment else "18px"};
    font-weight: 600;
    color: rgba(0, 0, 0, 0.9);
    line-height: {"20px" if is_comment else "22px"};
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  .verified-badge {{
    display: inline-flex;
    flex-shrink: 0;
  }}

  .actor-badge {{
    font-size: 12px;
    color: rgba(0, 0, 0, 0.6);
    font-weight: 400;
    white-space: nowrap;
  }}

  .actor-badge::before {{
    content: " · ";
  }}

  .actor-title {{
    font-size: 13px;
    font-weight: 400;
    color: rgba(0, 0, 0, 0.6);
    line-height: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-top: 1px;
  }}

  .actor-meta {{
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 2px;
  }}

  .actor-time {{
    font-size: 12px;
    color: rgba(0, 0, 0, 0.6);
    line-height: 14px;
  }}

  .globe-icon {{
    display: inline-flex;
    color: rgba(0, 0, 0, 0.6);
  }}

  .dots-btn {{
    margin-left: auto;
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px 6px;
    color: rgba(0, 0, 0, 0.6);
    flex-shrink: 0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  /* ── Post text ── */
  .post-text {{
    padding: {"8px 16px 4px" if is_comment else "10px 16px 6px"};
    font-size: {"14px" if is_comment else "15px"};
    font-weight: 400;
    color: rgba(0, 0, 0, 0.9);
    line-height: {"20px" if is_comment else "22px"};
  }}

  .post-text p {{
    margin: 0 0 8px 0;
  }}

  .post-text p:last-child {{
    margin-bottom: 0;
  }}

  /* ── Action bar ── */
  .action-bar {{
    display: flex;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    margin-top: 8px;
    padding: 0 4px;
  }}

  .action-btn {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 10px 4px;
    background: none;
    border: none;
    cursor: pointer;
    color: rgba(0, 0, 0, 0.6);
    font-size: 14px;
    font-weight: 600;
    font-family: inherit;
    border-radius: 4px;
  }}

  .action-icon {{
    display: inline-flex;
    color: rgba(0, 0, 0, 0.6);
  }}

  .action-label {{
    color: rgba(0, 0, 0, 0.6);
    font-size: 14px;
    font-weight: 600;
  }}

  /* ── Comment footer ── */
  .comment-actions {{
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 16px 10px;
  }}

  .comment-action-btn {{
    background: none;
    border: none;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
    color: rgba(0, 0, 0, 0.6);
    font-family: inherit;
    padding: 2px 4px;
    border-radius: 4px;
  }}

  .comment-dot {{
    font-size: 12px;
    color: rgba(0, 0, 0, 0.4);
  }}
</style>
</head>
<body>
<div class="{card_class}">

  <!-- Header -->
  <div class="header">
    <img class="avatar" src="{avatar_uri}" alt="{name}">
    <div class="actor-info">
      <div class="actor-name-row">
        <span class="actor-name">{name}</span>
        <span class="verified-badge">{SVG_VERIFIED}</span>
        <span class="actor-badge">{badge}</span>
      </div>
      <div class="actor-title">{title}</div>
      <div class="actor-meta">
        <span class="actor-time">{time_str}</span>
        <span class="globe-icon">{SVG_GLOBE}</span>
      </div>
    </div>
    <button class="dots-btn" aria-label="More options">
      {SVG_DOTS}
    </button>
  </div>

  <!-- Post text -->
  <div class="post-text">
    {text_html}
  </div>

  <!-- Actions -->
  {action_buttons}

</div>
</body>
</html>"""

    return html


def render_to_png(html: str, output_path: str, scale: int = 2) -> None:
    """Write HTML to temp file, screenshot with Playwright at 2x/3x Retina resolution."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        tmp_html = f.name

    script = f"""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={{"width": 560, "height": 600}},
            device_scale_factor={scale}
        )
        await page.goto("file://{tmp_html}")
        await page.wait_for_timeout(200)
        
        # Screenshot the card component directly for clean borders without extra body whitespace
        card = page.locator(".card")
        await card.screenshot(path="{output_path}")
        await browser.close()

asyncio.run(main())
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True, text=True
    )
    os.unlink(tmp_html)

    if result.returncode != 0:
        raise RuntimeError(f"Playwright error:\n{result.stderr}")


def main() -> None:
    ap = argparse.ArgumentParser(description="LinkedIn Screenshot Generator (HTML+Playwright)")
    ap.add_argument("--text",     required=True)
    ap.add_argument("--output",   required=True)
    ap.add_argument("--avatar",   required=True)
    ap.add_argument("--comment",  action="store_true", help="Render as comment card")
    ap.add_argument("--name",     default="Vitaliy Alhimovich")
    ap.add_argument("--title",    default="AI Engineer | Reduce manual work and get more leads using AI automations")
    ap.add_argument("--time",     default="3mo")
    args = ap.parse_args()

    html = build_html_post(
        text       = args.text,
        avatar_path= args.avatar,
        name       = args.name,
        title      = args.title,
        time_str   = args.time,
        is_comment = args.comment,
    )

    os.makedirs(Path(args.output).parent, exist_ok=True)
    render_to_png(html, args.output)
    print(f"✓ {args.output}")


if __name__ == "__main__":
    main()
