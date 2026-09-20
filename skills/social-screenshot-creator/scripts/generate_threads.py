#!/usr/bin/env python3
"""
Threads Screenshot Generator (HTML + Playwright)
Produces pixel-perfect 2x Retina screenshots of Threads posts.

Threads Dark UI Specs:
  - Background: #101010
  - Text:       #F3F3F3
  - Secondary:  #777777
  - Line / Sep: #2E2E2E
  - Card width: 560px
  - 2x Retina output

Usage:
  python3 generate_threads.py \
    --text "Post text here" \
    --output "/path/to/output.png" \
    --avatar "/path/to/avatar.jpg" \
    [--handle "ilovefiniki"] \
    [--time "2h"] \
    [--thread-num 1] \
    [--thread-total 3]
"""

import argparse
import base64
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# ── Threads SVG Icons (Clean Instagram / Threads Style) ────────────────────────

SVG_HEART = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
</svg>'''

SVG_COMMENT = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
</svg>'''

SVG_REPOST = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m17 2 4 4-4 4"/>
  <path d="M3 11V9a4 4 0 0 1 4-4h14"/>
  <path d="m7 22-4-4 4-4"/>
  <path d="M21 13v2a4 4 0 0 1-4 4H3"/>
</svg>'''

SVG_SHARE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="22" y1="2" x2="11" y2="13"/>
  <polygon points="22 2 15 22 11 13 2 9 22 2"/>
</svg>'''

SVG_DOTS = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
  <circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/>
</svg>'''


def avatar_to_data_uri(avatar_path: str) -> str:
    with open(avatar_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(avatar_path).suffix.lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
    return f"data:image/{mime};base64,{data}"


def build_html_threads(
    text: str,
    avatar_path: str,
    handle: str = "ilovefiniki",
    time_str: str = "2h",
    thread_num: int | None = None,
    thread_total: int | None = None,
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

    # Thread indicator
    thread_badge_html = ""
    if thread_num and thread_total:
        thread_badge_html = f"""
        <div class="thread-indicator">
          <span class="thread-num">({thread_num}/{thread_total})</span>
          <span class="thread-pill">{thread_num}/{thread_total}</span>
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
    background: #000000;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    padding: 8px;
    width: 480px;
  }}

  .threads-card {{
    background: #101010;
    border-radius: 12px;
    padding: 16px;
    display: flex;
    gap: 12px;
    position: relative;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.06);
  }}

  /* ── Left Column (Avatar + Thread Line) ── */
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

  .thread-line {{
    width: 2px;
    flex-grow: 1;
    background: #2E2E2E;
    margin-top: 8px;
    margin-bottom: 4px;
    border-radius: 1px;
    min-height: 20px;
  }}

  .thread-bottom-dots {{
    display: flex;
    align-items: center;
    gap: 3px;
    margin-top: 2px;
  }}

  .dot-sm {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #2E2E2E;
  }}

  .dot-xs {{
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #242424;
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
    margin-bottom: 6px;
  }}

  .handle-row {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .handle {{
    color: #F3F3F3;
    font-size: 15px;
    font-weight: 600;
    line-height: 18px;
  }}

  .timestamp {{
    color: #777777;
    font-size: 14px;
    font-weight: 400;
    line-height: 18px;
  }}

  .dots-menu {{
    color: #777777;
    cursor: pointer;
    display: flex;
    align-items: center;
  }}

  /* ── Post Text ── */
  .post-body {{
    color: #F3F3F3;
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

  /* ── Thread Indicator ── */
  .thread-indicator {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
  }}

  .thread-num {{
    color: #777777;
    font-size: 13px;
  }}

  .thread-pill {{
    background: #222222;
    color: #888888;
    font-size: 12px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 12px;
  }}

  /* ── Action Icons ── */
  .actions-row {{
    display: flex;
    align-items: center;
    gap: 18px;
    margin-top: 14px;
    color: #F3F3F3;
  }}

  .action-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
    color: #F3F3F3;
    opacity: 0.9;
  }}
</style>
</head>
<body>
<div class="threads-card">
  <!-- Left: Avatar + Connector line -->
  <div class="left-col">
    <img class="avatar" src="{avatar_uri}" alt="{handle}">
    <div class="thread-line"></div>
    <div class="thread-bottom-dots">
      <div class="dot-sm"></div>
      <div class="dot-xs"></div>
    </div>
  </div>

  <!-- Right: Header, Body, Actions -->
  <div class="right-col">
    <div class="header">
      <div class="handle-row">
        <span class="handle">{handle}</span>
        <span class="timestamp">{time_str}</span>
      </div>
      <div class="dots-menu">
        {SVG_DOTS}
      </div>
    </div>

    <div class="post-body">
      {text_html}
    </div>

    {thread_badge_html}

    <div class="actions-row">
      <div class="action-icon">{SVG_HEART}</div>
      <div class="action-icon">{SVG_COMMENT}</div>
      <div class="action-icon">{SVG_REPOST}</div>
      <div class="action-icon">{SVG_SHARE}</div>
    </div>
  </div>
</div>
</body>
</html>"""
    return html


def render_threads_png(html: str, output_path: str, scale: int = 2) -> None:
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
        
        card = page.locator(".threads-card")
        await card.screenshot(path="{output_path}")
        await browser.close()

asyncio.run(main())
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    os.unlink(tmp_html)

    if result.returncode != 0:
        raise RuntimeError(f"Playwright error:\n{result.stderr}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Threads Screenshot Generator (HTML + Playwright)")
    ap.add_argument("--text",         required=True)
    ap.add_argument("--output",       required=True)
    ap.add_argument("--avatar",       required=True)
    ap.add_argument("--handle",       default="ilovefiniki")
    ap.add_argument("--time",         default="2h")
    ap.add_argument("--thread-num",   type=int, default=None)
    ap.add_argument("--thread-total", type=int, default=None)
    ap.add_argument("--comment",      action="store_true")
    args = ap.parse_args()

    html = build_html_threads(
        text         = args.text,
        avatar_path  = args.avatar,
        handle       = args.handle,
        time_str     = args.time,
        thread_num   = args.thread_num,
        thread_total = args.thread_total,
        is_comment   = args.comment,
    )

    os.makedirs(Path(args.output).parent, exist_ok=True)
    render_threads_png(html, args.output, scale=2)
    print(f"✓ {args.output}")


if __name__ == "__main__":
    main()
