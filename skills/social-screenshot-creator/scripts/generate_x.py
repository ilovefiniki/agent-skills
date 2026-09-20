#!/usr/bin/env python3
"""
X (Twitter) Screenshot Generator (HTML + Playwright)
Produces pixel-perfect 2x Retina screenshots of X/Twitter posts & comments.

X / Twitter UI Specs:
  - Background: #000000 (Pure black)
  - Primary text: #E7E9EA
  - Secondary/meta: #71767B
  - Border/divider: #2F3336
  - Card width: 560px
  - 2x Retina output

Usage:
  python3 generate_x.py \
    --text "Post text here" \
    --output "/path/to/output.png" \
    --avatar "/path/to/avatar.jpg" \
    [--name "Vitaliy Alhimovich"] \
    [--handle "ilovefiniki"] \
    [--time "May 1"] \
    [--replies "1"] \
    [--views "4"] \
    [--verified] \
    [--comment]
"""

import argparse
import base64
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# ── X (Twitter) Official-style SVG Icons ─────────────────────────────────────

SVG_REPLY = '''<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
  <path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.25c-4.41 0-7.995-3.58-7.995-8.01zm8.005-6c-3.317 0-6.005 2.69-6.005 6 0 3.32 2.688 6.01 6.005 6.01h2.25v2.33l4.894-2.71c1.99-1.1 3.227-3.19 3.227-5.48 0-3.39-2.744-6.15-6.134-6.15H9.756z"/>
</svg>'''

SVG_RETWEET = '''<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
  <path d="M4.5 3.88l4.432 4.14-1.364 1.46L5.5 7.55V16c0 1.1.896 2 2 2H13v2H7.5c-2.209 0-4-1.79-4-4V7.55L1.432 9.48.068 8.02 4.5 3.88zM16.5 20.12l-4.432-4.14 1.364-1.46 2.068 1.93V8c0-1.1-.896-2-2-2H11V4h5.5c2.209 0 4 1.79 4 4v8.45l2.068-1.93 1.364 1.46-4.432 4.14z"/>
</svg>'''

SVG_LIKE = '''<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
  <path d="M16.697 5.5c-1.222-.06-2.679.51-3.89 2.16l-.805 1.09-.806-1.09C9.984 6.01 8.526 5.44 7.304 5.5c-2.415.11-4.304 2.18-4.304 4.74 0 2.06.945 3.99 2.587 5.37L12 21.03l6.413-5.42C20.055 14.23 21 12.3 21 10.24c0-2.56-1.889-4.63-4.303-4.74zM12 18.7l-4.992-4.22c-1.29-1.09-2.008-2.59-2.008-4.24 0-1.49 1.082-2.73 2.457-2.79.88-.04 1.94.39 2.873 1.66l1.67 2.27 1.67-2.27c.933-1.27 1.993-1.7 2.873-1.66 1.375.06 2.457 1.3 2.457 2.79 0 1.65-.718 3.15-2.008 4.24L12 18.7z"/>
</svg>'''

SVG_ANALYTICS = '''<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
  <path d="M8.75 21V3h2v18h-2zM18 21V8.5h2V21h-2zM4 21l.004-10h2L6 21H4zm9.248 0v-7h2v7h-2z"/>
</svg>'''

SVG_BOOKMARK = '''<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
  <path d="M4 4.5C4 3.12 5.119 2 6.5 2h11C18.881 2 20 3.12 20 4.5v18.44l-8-5.71-8 5.71V4.5zM6.5 4c-.276 0-.5.22-.5.5v14.56l6-4.29 6 4.29V4.5c0-.28-.224-.5-.5-.5h-11z"/>
</svg>'''

SVG_SHARE = '''<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
  <path d="M12 2.59l5.7 5.7-1.41 1.42L13 6.41V16h-2V6.41L7.71 9.71 6.3 8.29 12 2.59zM21 15l-.02 3.51c0 1.38-1.12 2.49-2.5 2.49H5.5C4.11 21.01 3 19.9 3 18.51V15h2v3.5c0 .28.22.5.5.5h12.98c.28 0 .5-.22.5-.5L19 15h2z"/>
</svg>'''

SVG_GROK = '''<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8 0-1.85.63-3.55 1.69-4.9L16.9 18.31C15.55 19.37 13.85 20 12 20zm6.31-3.1L7.1 5.69C8.45 4.63 10.15 4 12 4c4.41 0 8 3.59 8 8 0 1.85-.63 3.55-1.69 4.9z"/>
</svg>'''

SVG_DOTS = '''<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
  <path d="M3 12c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2zm9 2c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm7 0c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z"/>
</svg>'''

SVG_VERIFIED_BLUE = '''<svg viewBox="0 0 22 22" width="18" height="18" fill="none">
  <path d="M20.396 11a8.396 8.396 0 00-.541-2.975l-1.99 1.15a6.113 6.113 0 010 3.65l1.99 1.15A8.396 8.396 0 0020.396 11z" fill="#1D9BF0"/>
  <path d="M11 20.396a8.396 8.396 0 002.975-.541l-1.15-1.99a6.113 6.113 0 01-3.65 0l-1.15 1.99A8.396 8.396 0 0011 20.396z" fill="#1D9BF0"/>
  <path d="M1.604 11a8.396 8.396 0 00.541 2.975l1.99-1.15a6.113 6.113 0 010-3.65l-1.99-1.15A8.396 8.396 0 001.604 11z" fill="#1D9BF0"/>
  <path d="M11 1.604a8.396 8.396 0 00-2.975.541l1.15 1.99a6.113 6.113 0 013.65 0l1.15-1.99A8.396 8.396 0 0011 1.604z" fill="#1D9BF0"/>
  <path d="M9.64 14.58l-3.32-3.32 1.41-1.41 1.91 1.91 4.95-4.95 1.41 1.41-6.36 6.36z" fill="#FFFFFF"/>
</svg>'''


def avatar_to_data_uri(avatar_path: str) -> str:
    with open(avatar_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(avatar_path).suffix.lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
    return f"data:image/{mime};base64,{data}"


def build_html_x(
    text: str,
    avatar_path: str,
    name: str = "Vitaliy Alhimovich",
    handle: str = "ilovefiniki",
    time_str: str = "May 1",
    replies: str = "1",
    views: str = "4",
    verified: bool = True,
    is_comment: bool = False,
) -> str:
    avatar_uri = avatar_to_data_uri(avatar_path)

    # Format paragraphs
    blocks = re.split(r'\n\s*\n', text.strip())
    html_parts = []
    for block in blocks:
        lines = [l for l in block.split('\n')]
        rendered_block = "<br>".join(lines)
        if rendered_block.strip():
            html_parts.append(f"<p>{rendered_block}</p>")
    text_html = "\n".join(html_parts)

    verified_badge = f'<span class="verified-icon">{SVG_VERIFIED_BLUE}</span>' if verified else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=480">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: #000000;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    padding: 8px;
    width: 480px;
  }}

  .x-card {{
    background: #000000;
    border-radius: 12px;
    padding: 14px 16px 12px;
    display: flex;
    gap: 12px;
    box-shadow: 0 0 0 1px #2F3336;
  }}

  /* ── Left Column (Avatar) ── */
  .left-col {{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 40px;
    flex-shrink: 0;
  }}

  .avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
  }}

  /* ── Right Column (Content) ── */
  .right-col {{
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
  }}

  .header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
  }}

  .author-row {{
    display: flex;
    align-items: center;
    gap: 4px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }}

  .name {{
    color: #E7E9EA;
    font-size: 15px;
    font-weight: 700;
    line-height: 20px;
  }}

  .verified-icon {{
    display: inline-flex;
    align-items: center;
    flex-shrink: 0;
  }}

  .handle {{
    color: #71767B;
    font-size: 15px;
    font-weight: 400;
    line-height: 20px;
  }}

  .dot {{
    color: #71767B;
    font-size: 15px;
  }}

  .time {{
    color: #71767B;
    font-size: 15px;
    font-weight: 400;
    line-height: 20px;
  }}

  .header-actions {{
    display: flex;
    align-items: center;
    gap: 8px;
    color: #71767B;
    flex-shrink: 0;
  }}

  .header-icon {{
    display: flex;
    align-items: center;
    cursor: pointer;
  }}

  /* ── Post Body ── */
  .post-body {{
    color: #E7E9EA;
    font-size: 15px;
    font-weight: 400;
    line-height: 21px;
  }}

  .post-body p {{
    margin: 0 0 8px 0;
  }}

  .post-body p:last-child {{
    margin-bottom: 0;
  }}

  /* ── Engagement Action Bar ── */
  .actions-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 12px;
    max-width: 380px;
    color: #71767B;
  }}

  .action-btn {{
    display: flex;
    align-items: center;
    gap: 6px;
    color: #71767B;
    font-size: 13px;
    font-weight: 400;
    cursor: pointer;
  }}

  .action-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .action-count {{
    color: #71767B;
    font-size: 13px;
    line-height: 13px;
  }}
</style>
</head>
<body>
<div class="x-card">
  <!-- Left: Avatar -->
  <div class="left-col">
    <img class="avatar" src="{avatar_uri}" alt="{name}">
  </div>

  <!-- Right: Header, Body, Actions -->
  <div class="right-col">
    <div class="header">
      <div class="author-row">
        <span class="name">{name}</span>
        {verified_badge}
        <span class="handle">@{handle}</span>
        <span class="dot">·</span>
        <span class="time">{time_str}</span>
      </div>
      <div class="header-actions">
        <span class="header-icon">{SVG_GROK}</span>
        <span class="header-icon">{SVG_DOTS}</span>
      </div>
    </div>

    <div class="post-body">
      {text_html}
    </div>

    <div class="actions-row">
      <div class="action-btn">
        <div class="action-icon">{SVG_REPLY}</div>
        {f'<span class="action-count">{replies}</span>' if replies else ''}
      </div>
      <div class="action-btn">
        <div class="action-icon">{SVG_RETWEET}</div>
      </div>
      <div class="action-btn">
        <div class="action-icon">{SVG_LIKE}</div>
      </div>
      <div class="action-btn">
        <div class="action-icon">{SVG_BOOKMARK}</div>
      </div>
      <div class="action-btn">
        <div class="action-icon">{SVG_SHARE}</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""
    return html


def render_x_png(html: str, output_path: str, scale: int = 2) -> None:
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
        
        card = page.locator(".x-card")
        await card.screenshot(path="{output_path}")
        await browser.close()

asyncio.run(main())
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    os.unlink(tmp_html)

    if result.returncode != 0:
        raise RuntimeError(f"Playwright error:\n{result.stderr}")


def main() -> None:
    ap = argparse.ArgumentParser(description="X (Twitter) Screenshot Generator (HTML + Playwright)")
    ap.add_argument("--text",     required=True)
    ap.add_argument("--output",   required=True)
    ap.add_argument("--avatar",   required=True)
    ap.add_argument("--name",     default="Vitaliy Alhimovich")
    ap.add_argument("--handle",   default="ilovefiniki")
    ap.add_argument("--time",     default="May 1")
    ap.add_argument("--replies",  default="1")
    ap.add_argument("--views",    default="4")
    ap.add_argument("--verified", action="store_true", default=True)
    ap.add_argument("--comment",  action="store_true")
    args = ap.parse_args()

    html = build_html_x(
        text       = args.text,
        avatar_path= args.avatar,
        name       = args.name,
        handle     = args.handle,
        time_str   = args.time,
        replies    = args.replies,
        views      = args.views,
        verified   = args.verified,
        is_comment = args.comment,
    )

    os.makedirs(Path(args.output).parent, exist_ok=True)
    render_x_png(html, args.output, scale=2)
    print(f"✓ {args.output}")


if __name__ == "__main__":
    main()
