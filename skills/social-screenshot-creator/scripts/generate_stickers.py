#!/usr/bin/env python3
"""
Social Media Sticker / Quote Card Generator (Playwright + HTML)
Generates high-contrast, casually tilted "sticker cards" on a stylish canvas.
Supports dual or single card modes, and automatic fictional AI-generated personas.

Usage (dual quotes with automatic fictional personas):
  python3 generate_stickers.py \
    --card1-text "AI produces average results." \
    --card2-text "Only non-professionals like what AI makes." \
    --output "/path/to/output.png"

Usage (single quote):
  python3 generate_stickers.py \
    --mode single \
    --card1-text "AI made code cheap. The hardest decision is knowing when to stop." \
    --output "/path/to/single_quote.png"

Usage (specific personas or custom names):
  python3 generate_stickers.py \
    --card1-persona "alex_chen" \
    --card1-text "Why pay $20/month when you can build it in an evening?" \
    --card2-persona "sarah_jenkins" \
    --card2-text "Because maintenance costs $2,000/month." \
    --output "/path/to/output.png"
"""

import argparse
import base64
import json
import os
import random
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Watermark stripping helper
try:
    WM_DIR = Path(__file__).resolve().parent.parent.parent / "watermarks_remover"
    if str(WM_DIR) not in sys.path:
        sys.path.insert(0, str(WM_DIR))
    from clean_helper import clean_file_path
except ImportError:
    clean_file_path = None

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
PERSONAS_FILE = ASSETS_DIR / "personas.json"
AVATARS_DIR = ASSETS_DIR / "avatars"


def load_personas() -> list[dict]:
    if PERSONAS_FILE.exists():
        try:
            with open(PERSONAS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: could not load personas.json: {e}")
    return []


def get_persona(persona_id_or_random: str = "random", gender_filter: str = None, exclude_id: str = None) -> dict:
    personas = load_personas()
    if not personas:
        # Fallback default
        return {
            "id": "david_miller",
            "name": "David Miller",
            "handle": "davidmiller_dev",
            "role": "Senior Engineer",
            "avatar": "david_miller.jpg",
            "gender": "male"
        }

    if persona_id_or_random and persona_id_or_random != "random":
        for p in personas:
            if p["id"].lower() == persona_id_or_random.lower() or p["name"].lower() == persona_id_or_random.lower():
                return p

    candidates = personas
    if exclude_id:
        candidates = [p for p in candidates if p["id"] != exclude_id]
    if gender_filter:
        filtered = [p for p in candidates if p.get("gender") == gender_filter]
        if filtered:
            candidates = filtered

    return random.choice(candidates if candidates else personas)


def resolve_avatar_path(avatar_val: str) -> str:
    if not avatar_val:
        return str(AVATARS_DIR / "david_miller.jpg")
    p = Path(avatar_val)
    if p.is_file():
        return str(p)
    # Check in AVATARS_DIR
    in_avatars = AVATARS_DIR / avatar_val
    if in_avatars.is_file():
        return str(in_avatars)
    # Return default
    default_av = AVATARS_DIR / "david_miller.jpg"
    return str(default_av) if default_av.is_file() else avatar_val


def image_to_data_uri(path: str) -> str:
    resolved = resolve_avatar_path(path)
    if not Path(resolved).exists():
        # Fallback 1x1 transparent pixel
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    with open(resolved, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(resolved).suffix.lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
    return f"data:image/{mime};base64,{data}"


def build_sticker_html(card1: dict, card2: dict = None, mode: str = "dual", bg_style: str = "dot-grid") -> str:
    c1_uri = image_to_data_uri(card1["avatar"])
    c2_uri = image_to_data_uri(card2["avatar"]) if card2 else ""

    bg_css = """
      background: #F4F5F7;
      background-image: 
        radial-gradient(#D1D5DB 1.5px, transparent 1.5px),
        radial-gradient(#D1D5DB 1.5px, #F4F5F7 1.5px);
      background-size: 28px 28px;
      background-position: 0 0, 14px 14px;
    """
    if bg_style == "dark-dot-grid":
        bg_css = """
          background: #0F1115;
          background-image: 
            radial-gradient(#262B33 1.5px, transparent 1.5px),
            radial-gradient(#262B33 1.5px, #0F1115 1.5px);
          background-size: 28px 28px;
          background-position: 0 0, 14px 14px;
        """
    elif bg_style == "clean-light":
        bg_css = "background: #F8F9FA;"

    # Single card vs dual card positioning
    if mode == "single":
        card_layout_css = """
          .cards-container {
            position: relative;
            width: 1000px;
            height: 920px;
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .card-1 {
            position: relative;
            transform: rotate(-2.5deg);
            z-index: 1;
            margin: auto;
          }
          .card-2 {
            display: none;
          }
        """
    else:
        card_layout_css = """
          .cards-container {
            position: relative;
            width: 1000px;
            height: 920px;
          }
          .card-1 {
            top: 120px;
            left: 45px;
            transform: rotate(-4.2deg);
            z-index: 1;
          }
          .card-2 {
            top: 450px;
            left: 115px;
            transform: rotate(3.6deg);
            z-index: 2;
          }
        """

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    width: 1080px;
    height: 1080px;
    {bg_css}
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #E7E9EA;
    overflow: hidden;
  }}

  {card_layout_css}

  .card {{
    width: 840px;
    background: #000000;
    border: 1px solid #2F3336;
    border-radius: 26px;
    padding: 34px 40px;
    position: absolute;
    box-shadow: 
      0 12px 24px -6px rgba(0, 0, 0, 0.25),
      0 28px 56px -10px rgba(0, 0, 0, 0.45),
      0 0 0 1px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    gap: 20px;
  }}

  .header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .user-info {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .avatar {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
    border: 1px solid rgba(255, 255, 255, 0.12);
  }}

  .names {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .name-row {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .name {{
    font-weight: 700;
    font-size: 21px;
    color: #F7F9F9;
    letter-spacing: -0.2px;
  }}

  .verified {{
    width: 19px;
    height: 19px;
    color: #1D9BF0;
  }}

  .handle-row {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 16px;
    color: #71767B;
  }}

  .dots {{
    color: #71767B;
  }}

  .content {{
    font-size: 32px;
    line-height: 1.32;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: -0.3px;
  }}

  .actions {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 16px;
    border-top: 1px solid #1E2124;
    color: #71767B;
    font-size: 15px;
    font-weight: 500;
  }}

  .action-item {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .action-item svg {{
    width: 18px;
    height: 18px;
    fill: currentColor;
  }}
</style>
</head>
<body>

  <div class="cards-container">
    <!-- Card 1 -->
    <div class="card card-1">
      <div class="header">
        <div class="user-info">
          <img class="avatar" src="__CARD1_AVATAR__" alt="Avatar">
          <div class="names">
            <div class="name-row">
              <span class="name">__CARD1_NAME__</span>
              <svg class="verified" viewBox="0 0 22 22" fill="none">
                <path d="M20.396 11a8.396 8.396 0 00-.541-2.975l-1.99 1.15a6.113 6.113 0 010 3.65l1.99 1.15A8.396 8.396 0 0020.396 11z" fill="#1D9BF0"/>
                <path d="M11 20.396a8.396 8.396 0 002.975-.541l-1.15-1.99a6.113 6.113 0 01-3.65 0l-1.15 1.99A8.396 8.396 0 0011 20.396z" fill="#1D9BF0"/>
                <path d="M1.604 11a8.396 8.396 0 00.541 2.975l1.99-1.15a6.113 6.113 0 010-3.65l-1.99-1.15A8.396 8.396 0 001.604 11z" fill="#1D9BF0"/>
                <path d="M11 1.604a8.396 8.396 0 00-2.975.541l1.15 1.99a6.113 6.113 0 013.65 0l1.15-1.99A8.396 8.396 0 0011 1.604z" fill="#1D9BF0"/>
                <path d="M9.64 14.58l-3.32-3.32 1.41-1.41 1.91 1.91 4.95-4.95 1.41 1.41-6.36 6.36z" fill="#FFFFFF"/>
              </svg>
            </div>
            <div class="handle-row">
              <span>@__CARD1_HANDLE__</span>
              <span>·</span>
              <span>__CARD1_TIME__</span>
            </div>
          </div>
        </div>
        <div class="dots">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M3 12c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2zm9 2c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm7 0c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z"/>
          </svg>
        </div>
      </div>
      <div class="content">
        __CARD1_TEXT__
      </div>
      <div class="actions">
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.25c-4.41 0-7.995-3.58-7.995-8.01zm8.005-6c-3.317 0-6.005 2.69-6.005 6 0 3.32 2.688 6.01 6.005 6.01h2.25v2.33l4.894-2.71c1.99-1.1 3.227-3.19 3.227-5.48 0-3.39-2.744-6.15-6.134-6.15H9.756z"/></svg>
          <span>__CARD1_REPLIES__</span>
        </div>
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M4.5 3.88l4.432 4.14-1.364 1.46L5.5 7.55V16c0 1.1.896 2 2 2H13v2H7.5c-2.209 0-4-1.79-4-4V7.55L1.432 9.48.068 8.02 4.5 3.88zM16.5 20.12l-4.432-4.14 1.364-1.46 2.068 1.93V8c0-1.1-.896-2-2-2H11V4h5.5c2.209 0 4 1.79 4 4v8.45l2.068-1.93 1.364 1.46-4.432 4.14z"/></svg>
          <span>__CARD1_RETWEETS__</span>
        </div>
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M16.697 5.5c-1.222-.06-2.679.51-3.89 2.16l-.805 1.09-.806-1.09C9.984 6.01 8.526 5.44 7.304 5.5c-2.415.11-4.304 2.18-4.304 4.74 0 2.06.945 3.99 2.587 5.37L12 21.03l6.413-5.42C20.055 14.23 21 12.3 21 10.24c0-2.56-1.889-4.63-4.303-4.74zM12 18.7l-4.992-4.22c-1.29-1.09-2.008-2.59-2.008-4.24 0-1.49 1.082-2.73 2.457-2.79.88-.04 1.94.39 2.873 1.66l1.67 2.27 1.67-2.27c.933-1.27 1.993-1.7 2.873-1.66 1.375.06 2.457 1.3 2.457 2.79 0 1.65-.718 3.15-2.008 4.24L12 18.7z"/></svg>
          <span>__CARD1_LIKES__</span>
        </div>
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M8.75 21V3h2v18h-2zM18 21V8.5h2V21h-2zM4 21l.004-10h2L6 21H4zm9.248 0v-7h2v7h-2z"/></svg>
          <span>__CARD1_VIEWS__</span>
        </div>
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M12 2.59l5.7 5.7-1.41 1.42L13 6.41V16h-2V6.41L7.71 9.71 6.3 8.29 12 2.59zM21 15l-.02 3.51c0 1.38-1.12 2.49-2.5 2.49H5.5C4.11 21.01 3 19.9 3 18.51V15h2v3.5c0 .28.22.5.5.5h12.98c.28 0 .5-.22.5-.5L19 15h2z"/></svg>
        </div>
      </div>
    </div>

    <!-- Card 2 -->
    <div class="card card-2">
      <div class="header">
        <div class="user-info">
          <img class="avatar" src="__CARD2_AVATAR__" alt="Avatar">
          <div class="names">
            <div class="name-row">
              <span class="name">__CARD2_NAME__</span>
              <svg class="verified" viewBox="0 0 22 22" fill="none">
                <path d="M20.396 11a8.396 8.396 0 00-.541-2.975l-1.99 1.15a6.113 6.113 0 010 3.65l1.99 1.15A8.396 8.396 0 0020.396 11z" fill="#1D9BF0"/>
                <path d="M11 20.396a8.396 8.396 0 002.975-.541l-1.15-1.99a6.113 6.113 0 01-3.65 0l-1.15 1.99A8.396 8.396 0 0011 20.396z" fill="#1D9BF0"/>
                <path d="M1.604 11a8.396 8.396 0 00.541 2.975l1.99-1.15a6.113 6.113 0 010-3.65l-1.99-1.15A8.396 8.396 0 001.604 11z" fill="#1D9BF0"/>
                <path d="M11 1.604a8.396 8.396 0 00-2.975.541l1.15 1.99a6.113 6.113 0 013.65 0l1.15-1.99A8.396 8.396 0 0011 1.604z" fill="#1D9BF0"/>
                <path d="M9.64 14.58l-3.32-3.32 1.41-1.41 1.91 1.91 4.95-4.95 1.41 1.41-6.36 6.36z" fill="#FFFFFF"/>
              </svg>
            </div>
            <div class="handle-row">
              <span>@__CARD2_HANDLE__</span>
              <span>·</span>
              <span>__CARD2_TIME__</span>
            </div>
          </div>
        </div>
        <div class="dots">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M3 12c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2zm9 2c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm7 0c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z"/>
          </svg>
        </div>
      </div>
      <div class="content">
        __CARD2_TEXT__
      </div>
      <div class="actions">
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.25c-4.41 0-7.995-3.58-7.995-8.01zm8.005-6c-3.317 0-6.005 2.69-6.005 6 0 3.32 2.688 6.01 6.005 6.01h2.25v2.33l4.894-2.71c1.99-1.1 3.227-3.19 3.227-5.48 0-3.39-2.744-6.15-6.134-6.15H9.756z"/></svg>
          <span>__CARD2_REPLIES__</span>
        </div>
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M4.5 3.88l4.432 4.14-1.364 1.46L5.5 7.55V16c0 1.1.896 2 2 2H13v2H7.5c-2.209 0-4-1.79-4-4V7.55L1.432 9.48.068 8.02 4.5 3.88zM16.5 20.12l-4.432-4.14 1.364-1.46 2.068 1.93V8c0-1.1-.896-2-2-2H11V4h5.5c2.209 0 4 1.79 4 4v8.45l2.068-1.93 1.364 1.46-4.432 4.14z"/></svg>
          <span>__CARD2_RETWEETS__</span>
        </div>
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M16.697 5.5c-1.222-.06-2.679.51-3.89 2.16l-.805 1.09-.806-1.09C9.984 6.01 8.526 5.44 7.304 5.5c-2.415.11-4.304 2.18-4.304 4.74 0 2.06.945 3.99 2.587 5.37L12 21.03l6.413-5.42C20.055 14.23 21 12.3 21 10.24c0-2.56-1.889-4.63-4.303-4.74zM12 18.7l-4.992-4.22c-1.29-1.09-2.008-2.59-2.008-4.24 0-1.49 1.082-2.73 2.457-2.79.88-.04 1.94.39 2.873 1.66l1.67 2.27 1.67-2.27c.933-1.27 1.993-1.7 2.873-1.66 1.375.06 2.457 1.3 2.457 2.79 0 1.65-.718 3.15-2.008 4.24L12 18.7z"/></svg>
          <span>__CARD2_LIKES__</span>
        </div>
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M8.75 21V3h2v18h-2zM18 21V8.5h2V21h-2zM4 21l.004-10h2L6 21H4zm9.248 0v-7h2v7h-2z"/></svg>
          <span>__CARD2_VIEWS__</span>
        </div>
        <div class="action-item">
          <svg viewBox="0 0 24 24"><path d="M12 2.59l5.7 5.7-1.41 1.42L13 6.41V16h-2V6.41L7.71 9.71 6.3 8.29 12 2.59zM21 15l-.02 3.51c0 1.38-1.12 2.49-2.5 2.49H5.5C4.11 21.01 3 19.9 3 18.51V15h2v3.5c0 .28.22.5.5.5h12.98c.28 0 .5-.22.5-.5L19 15h2z"/></svg>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""
    replacements = {
        "__CARD1_AVATAR__": c1_uri,
        "__CARD1_NAME__": card1.get("name", "David Miller"),
        "__CARD1_HANDLE__": card1.get("handle", "davidmiller_dev"),
        "__CARD1_TIME__": card1.get("time", "4h"),
        "__CARD1_TEXT__": card1.get("text", "AI produces average results."),
        "__CARD1_REPLIES__": card1.get("replies", "48"),
        "__CARD1_RETWEETS__": card1.get("retweets", "19"),
        "__CARD1_LIKES__": card1.get("likes", "412"),
        "__CARD1_VIEWS__": card1.get("views", "32.4K"),
    }

    if card2:
        replacements.update({
            "__CARD2_AVATAR__": c2_uri,
            "__CARD2_NAME__": card2.get("name", "Sarah Jenkins"),
            "__CARD2_HANDLE__": card2.get("handle", "sarahj_design"),
            "__CARD2_TIME__": card2.get("time", "6h"),
            "__CARD2_TEXT__": card2.get("text", "Only non-professionals like what AI makes."),
            "__CARD2_REPLIES__": card2.get("replies", "92"),
            "__CARD2_RETWEETS__": card2.get("retweets", "37"),
            "__CARD2_LIKES__": card2.get("likes", "740"),
            "__CARD2_VIEWS__": card2.get("views", "58.9K"),
        })

    for k, v in replacements.items():
        html_template = html_template.replace(k, str(v))

    return html_template


def generate_stickers_image(card1: dict, card2: dict = None, mode: str = "dual", bg_style: str = "dot-grid", output_path: str = ""):
    html_content = build_sticker_html(card1, card2, mode=mode, bg_style=bg_style)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1080, "height": 1080},
            device_scale_factor=2
        )
        page.set_content(html_content)
        page.wait_for_timeout(500)
        page.screenshot(path=output_path, type="png")
        browser.close()

    # Clean metadata & watermarks
    if clean_file_path:
        clean_file_path(output_path, in_place=True)

    print(f"Stickers visual generated & cleaned: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate tilted sticker quote cards visual with fictional personas")
    parser.add_argument("--mode", choices=["dual", "single"], default="dual", help="Card layout mode: dual (default) or single")
    parser.add_argument("--bg-style", choices=["dot-grid", "dark-dot-grid", "clean-light"], default="dot-grid")

    # Card 1 options
    parser.add_argument("--card1-text", required=True, help="Text for card 1")
    parser.add_argument("--card1-persona", default=None, help="Persona ID or 'random'")
    parser.add_argument("--card1-name", default=None)
    parser.add_argument("--card1-handle", default=None)
    parser.add_argument("--card1-avatar", default=None)
    parser.add_argument("--card1-time", default="4h")
    parser.add_argument("--card1-replies", default="48")
    parser.add_argument("--card1-retweets", default="19")
    parser.add_argument("--card1-likes", default="412")
    parser.add_argument("--card1-views", default="32.4K")

    # Card 2 options (required if mode == dual)
    parser.add_argument("--card2-text", default=None, help="Text for card 2")
    parser.add_argument("--card2-persona", default=None, help="Persona ID or 'random'")
    parser.add_argument("--card2-name", default=None)
    parser.add_argument("--card2-handle", default=None)
    parser.add_argument("--card2-avatar", default=None)
    parser.add_argument("--card2-time", default="6h")
    parser.add_argument("--card2-replies", default="92")
    parser.add_argument("--card2-retweets", default="37")
    parser.add_argument("--card2-likes", default="740")
    parser.add_argument("--card2-views", default="58.9K")

    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    # Resolve Card 1 Persona
    p1 = get_persona(persona_id_or_random=args.card1_persona or "random", gender_filter="male")
    c1 = {
        "text": args.card1_text,
        "name": args.card1_name or p1["name"],
        "handle": args.card1_handle or p1["handle"],
        "avatar": args.card1_avatar or p1["avatar"],
        "time": args.card1_time,
        "replies": args.card1_replies,
        "retweets": args.card1_retweets,
        "likes": args.card1_likes,
        "views": args.card1_views,
    }

    c2 = None
    if args.mode == "dual":
        card2_text = args.card2_text if args.card2_text else "Only non-professionals like what AI makes."
        p2 = get_persona(persona_id_or_random=args.card2_persona or "random", gender_filter="female", exclude_id=p1.get("id"))
        c2 = {
            "text": card2_text,
            "name": args.card2_name or p2["name"],
            "handle": args.card2_handle or p2["handle"],
            "avatar": args.card2_avatar or p2["avatar"],
            "time": args.card2_time,
            "replies": args.card2_replies,
            "retweets": args.card2_retweets,
            "likes": args.card2_likes,
            "views": args.card2_views,
        }

    # Ensure output dir exists
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    generate_stickers_image(c1, c2, mode=args.mode, bg_style=args.bg_style, output_path=args.output)
