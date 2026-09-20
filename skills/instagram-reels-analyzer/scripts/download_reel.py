#!/usr/bin/env python3
"""
Instagram Reels Downloader with Built-in Rate Limiting & Zero Account Risk.
Downloads public Instagram Reels without authentication cookies.
"""

import sys
import os
import json
import time
import argparse
from pathlib import Path
import subprocess

STATE_FILE = Path.home() / ".cache" / "reels_rate_limit.json"

# Rate limiting defaults
MAX_REELS_PER_HOUR = 10
MIN_COOLDOWN_SECONDS = 15  # Pause between back-to-back downloads


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"history": []}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def check_rate_limits(max_per_hour=MAX_REELS_PER_HOUR, min_cooldown=MIN_COOLDOWN_SECONDS):
    state = load_state()
    now = time.time()
    one_hour_ago = now - 3600

    # Clean up records older than 1 hour
    recent_history = [t for t in state.get("history", []) if t > one_hour_ago]
    state["history"] = recent_history

    # Check cooldown between successive downloads
    if recent_history:
        last_download = max(recent_history)
        elapsed = now - last_download
        if elapsed < min_cooldown:
            wait_needed = int(min_cooldown - elapsed)
            return False, f"Cooldown active: please wait {wait_needed}s before downloading another Reel to avoid IP blocks.", state

    # Check hourly limit
    if len(recent_history) >= max_per_hour:
        oldest_in_window = min(recent_history)
        reset_wait = int(3600 - (now - oldest_in_window))
        return False, f"Rate limit reached ({len(recent_history)}/{max_per_hour} reels in the last hour). Resets in {reset_wait // 60}m {reset_wait % 60}s.", state

    return True, None, state


def record_download(state: dict):
    state["history"].append(time.time())
    save_state(state)


def download_reel(url: str, output_dir: str) -> dict:
    # Clean up URL parameters (remove tracking params like utm_source, stkn)
    clean_url = url.split("?")[0].rstrip("/")
    if not clean_url.endswith("/"):
        clean_url += "/"

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    output_template = str(out_path / "%(id)s.%(ext)s")

    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--no-playlist",
        "-o",
        output_template,
        "--print-json",
        clean_url,
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        err_msg = res.stderr or res.stdout
        if "login required" in err_msg.lower() or "rate-limit" in err_msg.lower():
            return {
                "success": False,
                "error": "Instagram temporarily restricted anonymous access from this IP or requires login.",
                "details": err_msg.strip(),
            }
        return {"success": False, "error": f"yt-dlp error: {err_msg.strip()}"}

    # Parse metadata from stdout
    try:
        metadata = json.loads(res.stdout.strip().splitlines()[-1])
        video_id = metadata.get("id")
        ext = metadata.get("ext", "mp4")
        final_file = out_path / f"{video_id}.{ext}"

        # If extension changed during merge
        if not final_file.exists():
            mp4_file = out_path / f"{video_id}.mp4"
            if mp4_file.exists():
                final_file = mp4_file

        return {
            "success": True,
            "file_path": str(final_file.resolve()),
            "id": video_id,
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "uploader": metadata.get("uploader", ""),
            "duration": metadata.get("duration", 0),
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to parse yt-dlp response: {e}"}


def main():
    parser = argparse.ArgumentParser(description="Instagram Reels Downloader with Rate Limiter")
    parser.add_argument("url", help="Instagram Reel URL")
    parser.add_argument("--output-dir", default="./scratch", help="Directory to save downloaded video")
    parser.add_argument("--max-per-hour", type=int, default=MAX_REELS_PER_HOUR, help="Max reels allowed per hour")
    parser.add_argument("--force", action="store_true", help="Bypass rate limiting")

    args = parser.parse_args()

    if not args.force:
        allowed, reason, state = check_rate_limits(max_per_hour=args.max_per_hour)
        if not allowed:
            print(json.dumps({"success": False, "error": reason, "rate_limited": True}, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        state = load_state()

    result = download_reel(args.url, args.output_dir)
    if result.get("success"):
        record_download(state)
        # Add remaining quota info
        now = time.time()
        active_count = len([t for t in state["history"] if t > now - 3600])
        result["quota"] = {
            "used_last_hour": active_count,
            "max_per_hour": args.max_per_hour,
            "remaining": max(0, args.max_per_hour - active_count),
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
