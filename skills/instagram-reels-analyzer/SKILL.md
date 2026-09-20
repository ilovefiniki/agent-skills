---
name: instagram-reels-analyzer
description: "Download, inspect, and summarize Instagram Reels locally with zero personal account risk and built-in rate-limiting guards. Use whenever the user provides an Instagram Reel link or asks to inspect, summarize, or transcribe an Instagram Reel."
---

# Instagram Reels Analyzer

Downloads public Instagram Reels safely without authenticating to any personal Instagram account (0% account ban risk), respects IP rate limits, and performs multimodal video, speech, and on-screen text analysis locally.

---

## 🛡️ Safety & Rate Limiting Rules

1. **Zero Personal Credentials:** Never asks for or uses personal Instagram credentials or cookies. All downloads are performed anonymously.
2. **Built-in Rate Guard:**
   - Maximum **10 Reels per hour** (rolling 60-minute window).
   - Mandatory **15-second cooldown** between consecutive downloads.
   - Guard state is maintained in `~/.cache/reels_rate_limit.json`.
3. **Graceful Handling on Limit:** If the rate limit is hit, informs the user of the exact reset cooldown without crashing.

---

## 🚀 Execution Workflow

### Step 1: Download with Rate Limiting
Run the downloader script passing the Reel URL and an output directory:

```bash
python3 scripts/download_reel.py "<INSTAGRAM_REEL_URL>" --output-dir "./output"
```

The script outputs structured JSON:
```json
{
  "success": true,
  "file_path": "/path/to/video.mp4",
  "id": "C7xxxxxx",
  "title": "...",
  "uploader": "username",
  "duration": 28
}
```

### Step 2: Multimodal Video & Audio Inspection
Use local video inspection tools or ffmpeg/whisper to extract:
1. **On-Screen Text (OCR):** Subtitles, key text overlays, and hooks.
2. **Visual Progression:** Scene transitions, product demonstrations, and visual actions.
3. **Spoken Dialogue:** Full spoken transcript.

### Step 3: Structured Output Format

```markdown
### 🎬 Instagram Reel Breakdown

* **Creator:** @{uploader}
* **Duration:** {duration}s
* **Quota Remaining:** {remaining}/{max_per_hour}

---

#### 🎯 Hook & Core Thesis
{1-2 sentences explaining what the Reel is about and why it hooks attention}

#### 👁️ On-Screen Text (Captions / Overlays)
> "{Verbatim text overlays and on-screen cards}"

#### 🎞️ Visual Sequence & Scene Pacing
1. **00:00 - 00:03:** {Hook shot, visual setup, movement}
2. **00:04 - 00:15:** {Core demonstration / storytelling}
3. **00:16 - end:** {CTA, ending frame}

#### 💡 Key Takeaways
* {Insight 1}
* {Insight 2}
```
