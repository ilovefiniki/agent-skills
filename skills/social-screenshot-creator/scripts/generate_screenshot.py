#!/usr/bin/env python3
"""
Social Media Screenshot Generator v3.0 (HTML + Playwright 2x Retina)
Generates 100% pixel-perfect screenshots of LinkedIn, Threads, and X/Twitter posts & comments.

Platforms:
  - LinkedIn (Light theme, authentic DOM specs & SVGs)
  - Threads (Dark theme #101010, left thread line, verified SVG icons)
  - X / Twitter (Pure black #000000, official vector SVGs & engagement row)

Output:
  YYYY-MM-DD_slug/
    ├── linkedin_post.png
    ├── threads_post.png
    ├── x_post.png
    ├── linkedin_comment.png  (if --comment provided)
    ├── threads_comment.png
    └── x_comment.png

Usage:
  python3 generate_screenshot.py \
    --text "Your post text" \
    --comment "Optional comment text" \
    --output-dir "/path/to/screenshots" \
    --avatar "/path/to/avatar.jpg"
"""

import argparse
import asyncio
import base64
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# Import builder functions from modules
from generate_linkedin import build_html_post as build_linkedin_html
from generate_threads import build_html_threads
from generate_x import build_html_x


def slugify(text: str, max_words: int = 5) -> str:
    clean = re.sub(r"[^\w\s-]", "", text).strip().lower()
    words = clean.split()[:max_words]
    return "-".join(words) if words else "post"


async def render_batch(jobs: list[tuple[str, str]], scale: int = 2) -> list[str]:
    """
    Renders multiple HTML strings to PNGs in a single browser session for max speed.
    jobs: list of (html_content, output_path)
    """
    output_files = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 480, "height": 600},
            device_scale_factor=scale
        )

        for html_content, output_path in jobs:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
                f.write(html_content)
                tmp_file = f.name

            try:
                await page.goto(f"file://{tmp_file}")
                await page.wait_for_timeout(150)
                
                # Target the card element
                card = page.locator(".card, .threads-card, .x-card")
                if await card.count() > 0:
                    await card.first.screenshot(path=output_path)
                else:
                    await page.screenshot(path=output_path, full_page=True)
                output_files.append(output_path)
                print(f"  ✓ {Path(output_path).name}")
            finally:
                if os.path.exists(tmp_file):
                    os.unlink(tmp_file)

        await browser.close()
    return output_files


def generate_all(
    text: str,
    avatar_path: str,
    base_dir: str,
    name: str = "Vitaliy Alhimovich",
    handle: str = "ilovefiniki",
    title: str = "AI Engineer | Reduce manual work and get more leads using AI automations",
    slug: str | None = None,
    comment: str | None = None,
    li_time: str = "1d",
    th_time: str = "2h",
    x_time: str = "May 1",
) -> tuple[str, list[str]]:
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_slug = slug or slugify(text)
    out_dir = Path(base_dir) / f"{date_str}_{folder_slug}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nRendering 2x Retina screenshots for: {folder_slug}")

    jobs = [
        (
            build_linkedin_html(text, avatar_path, name=name, title=title, time_str=li_time, is_comment=False),
            str(out_dir / "linkedin_post.png"),
        ),
        (
            build_html_threads(text, avatar_path, handle=handle, time_str=th_time, thread_num=1, thread_total=3, is_comment=False),
            str(out_dir / "threads_post.png"),
        ),
        (
            build_html_x(text, avatar_path, name=name, handle=handle, time_str=x_time, replies="1", views="4", verified=True, is_comment=False),
            str(out_dir / "x_post.png"),
        ),
    ]

    if comment:
        jobs.extend([
            (
                build_linkedin_html(comment, avatar_path, name=name, title=title, time_str=li_time, is_comment=True),
                str(out_dir / "linkedin_comment.png"),
            ),
            (
                build_html_threads(comment, avatar_path, handle=handle, time_str=th_time, is_comment=True),
                str(out_dir / "threads_comment.png"),
            ),
            (
                build_html_x(comment, avatar_path, name=name, handle=handle, time_str=x_time, replies="", views="9", verified=True, is_comment=True),
                str(out_dir / "x_comment.png"),
            ),
        ])

    generated = asyncio.run(render_batch(jobs, scale=2))
    print(f"\nDone! {len(generated)} image(s) saved to:")
    print(f"  {out_dir}")
    return str(out_dir), generated


def main() -> None:
    default_avatar = str(Path(__file__).resolve().parent.parent / "assets" / "default_avatar.png")
    ap = argparse.ArgumentParser(description="Social Media Screenshot Generator (Playwright 2x Retina)")
    ap.add_argument("--text",         required=True, help="Post text content")
    ap.add_argument("--comment",      default=None, help="Optional comment text")
    ap.add_argument("--output-dir",   default="./screenshots", help="Directory to save generated screenshots")
    ap.add_argument("--avatar",       default=default_avatar, help="Path to avatar image file")
    ap.add_argument("--slug",         default=None, help="Custom folder slug name")
    ap.add_argument("--name",         default="Alex Rivers", help="Display name")
    ap.add_argument("--handle",       default="alexrivers", help="Social handle")
    ap.add_argument("--title",        default="AI Engineer & Systems Architect", help="Headline / Bio title")
    ap.add_argument("--li-time",      default="1d")
    ap.add_argument("--threads-time", default="2h")
    ap.add_argument("--x-time",       default="May 1")
    args = ap.parse_args()

    generate_all(
        text       = args.text,
        avatar_path= args.avatar,
        base_dir   = args.output_dir,
        name       = args.name,
        handle     = args.handle,
        title      = args.title,
        slug       = args.slug,
        comment    = args.comment,
        li_time    = args.li_time,
        th_time    = args.threads_time,
        x_time     = args.x_time,
    )


if __name__ == "__main__":
    main()
