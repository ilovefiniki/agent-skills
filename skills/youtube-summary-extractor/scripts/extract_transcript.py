#!/usr/bin/env python3
"""
YouTube Video Transcript & Metadata Extractor with Rate Limiting.
Zero video download: fetches subtitles & chapters in seconds.
"""

import sys
import os
import re
import json
import time
import argparse
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

STATE_FILE = Path.home() / ".cache" / "youtube_rate_limit.json"
MAX_REQUESTS_PER_HOUR = 20
MIN_COOLDOWN_SECONDS = 5


def extract_video_id(url_or_id: str) -> str:
    """Extract 11-char YouTube video ID from various URL formats or raw ID."""
    if len(url_or_id) == 11 and re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id

    patterns = [
        r"(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/shorts\/|\/live\/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    return ""


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


def check_rate_limits(max_per_hour=MAX_REQUESTS_PER_HOUR, min_cooldown=MIN_COOLDOWN_SECONDS):
    state = load_state()
    now = time.time()
    one_hour_ago = now - 3600

    recent_history = [t for t in state.get("history", []) if t > one_hour_ago]
    state["history"] = recent_history

    if recent_history:
        last_req = max(recent_history)
        elapsed = now - last_req
        if elapsed < min_cooldown:
            wait_needed = int(min_cooldown - elapsed)
            return False, f"Cooldown active: please wait {wait_needed}s before processing another video.", state

    if len(recent_history) >= max_per_hour:
        oldest = min(recent_history)
        reset_wait = int(3600 - (now - oldest))
        return False, f"Rate limit reached ({len(recent_history)}/{max_per_hour} videos/hr). Resets in {reset_wait // 60}m.", state

    return True, None, state


def record_request(state: dict):
    state["history"].append(time.time())
    save_state(state)


def format_timestamp(seconds: float) -> str:
    s = int(seconds)
    hours = s // 3600
    minutes = (s % 3600) // 60
    secs = s % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def get_metadata(video_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    meta = {
        "title": f"YouTube Video ({video_id})",
        "channel": "",
        "duration": 0,
        "description": "",
        "chapters": [],
    }
    if not yt_dlp:
        return meta

    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                meta["title"] = info.get("title", meta["title"])
                meta["channel"] = info.get("uploader", "") or info.get("channel", "")
                meta["duration"] = info.get("duration", 0)
                meta["description"] = (info.get("description", "") or "")[:1000]

                chapters = info.get("chapters")
                if chapters:
                    meta["chapters"] = [
                        {
                            "title": ch.get("title", ""),
                            "start_time": ch.get("start_time", 0),
                            "start_formatted": format_timestamp(ch.get("start_time", 0)),
                        }
                        for ch in chapters
                    ]
    except Exception:
        pass
    return meta


def get_transcript(video_id: str) -> dict:
    if not YouTubeTranscriptApi:
        return {"success": False, "error": "youtube_transcript_api is not installed"}

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        # Look for priority languages: ru, en, or first available
        target_transcript = None
        for lang_code in ["ru", "en"]:
            try:
                target_transcript = transcript_list.find_transcript([lang_code])
                if target_transcript:
                    break
            except Exception:
                continue

        if not target_transcript:
            for t in transcript_list:
                target_transcript = t
                break

        if not target_transcript:
            return {"success": False, "error": "No transcripts found for this video"}

        fetched = target_transcript.fetch()
        snippets = getattr(fetched, "snippets", fetched)

        # Group snippets into timed segments (~60-90 seconds chunks)
        chunks = []
        current_chunk = {"start": 0, "start_formatted": "00:00", "texts": []}
        full_text_parts = []

        chunk_window = 60.0  # seconds per group

        for item in snippets:
            text = (getattr(item, "text", None) or item.get("text", "")).strip()
            start = getattr(item, "start", None) or item.get("start", 0.0)

            if not text:
                continue

            full_text_parts.append(text)

            if start - current_chunk["start"] >= chunk_window and current_chunk["texts"]:
                chunks.append({
                    "timestamp": current_chunk["start_formatted"],
                    "seconds": int(current_chunk["start"]),
                    "text": " ".join(current_chunk["texts"])
                })
                current_chunk = {
                    "start": start,
                    "start_formatted": format_timestamp(start),
                    "texts": [text],
                }
            else:
                if not current_chunk["texts"]:
                    current_chunk["start"] = start
                    current_chunk["start_formatted"] = format_timestamp(start)
                current_chunk["texts"].append(text)

        if current_chunk["texts"]:
            chunks.append({
                "timestamp": current_chunk["start_formatted"],
                "seconds": int(current_chunk["start"]),
                "text": " ".join(current_chunk["texts"])
            })

        return {
            "success": True,
            "language": target_transcript.language,
            "language_code": target_transcript.language_code,
            "is_generated": target_transcript.is_generated,
            "chunks": chunks,
            "full_text": " ".join(full_text_parts),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube Transcript and Structure")
    parser.add_argument("url", help="YouTube video URL or Video ID")
    parser.add_argument("--max-per-hour", type=int, default=MAX_REQUESTS_PER_HOUR, help="Max requests/hr")
    parser.add_argument("--force", action="store_true", help="Bypass rate limit")

    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        print(json.dumps({"success": False, "error": "Invalid YouTube URL or video ID"}, ensure_ascii=False))
        sys.exit(1)

    if not args.force:
        allowed, reason, state = check_rate_limits(max_per_hour=args.max_per_hour)
        if not allowed:
            print(json.dumps({"success": False, "error": reason, "rate_limited": True}, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        state = load_state()

    # Extract metadata + transcript
    meta = get_metadata(video_id)
    transcript_res = get_transcript(video_id)

    if not transcript_res.get("success"):
        print(json.dumps({
            "success": False,
            "video_id": video_id,
            "metadata": meta,
            "error": transcript_res.get("error", "Failed to retrieve transcript")
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    record_request(state)

    now = time.time()
    active_count = len([t for t in state["history"] if t > now - 3600])

    response = {
        "success": True,
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "title": meta.get("title"),
        "channel": meta.get("channel"),
        "duration_seconds": meta.get("duration"),
        "duration_formatted": format_timestamp(meta.get("duration", 0)),
        "chapters": meta.get("chapters", []),
        "language": transcript_res.get("language"),
        "language_code": transcript_res.get("language_code"),
        "is_generated_subtitles": transcript_res.get("is_generated"),
        "chunks_count": len(transcript_res.get("chunks", [])),
        "chunks": transcript_res.get("chunks", []),
        "full_text": transcript_res.get("full_text", ""),
        "quota": {
            "used_last_hour": active_count,
            "max_per_hour": args.max_per_hour,
            "remaining": max(0, args.max_per_hour - active_count),
        }
    }

    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
