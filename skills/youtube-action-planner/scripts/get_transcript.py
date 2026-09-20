import sys
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

def extract_video_id(url_or_id):
    if len(url_or_id) == 11:
        return url_or_id
    # Handle various YouTube URL formats
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:embed\/)([0-9A-Za-z_-]{11})",
        r"(?:be\/)([0-9A-Za-z_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return None

def get_transcript(video_id):
    try:
        # Correct pattern for this version of the library
        api = YouTubeTranscriptApi()
        try:
            segments = api.fetch(video_id)
            return " ".join(s.text.strip() for s in segments)
        except:
            # Fallback to list()
            transcript_list = api.list(video_id)
            transcript = next(iter(transcript_list))
            segments = transcript.fetch()
            return " ".join(s.text.strip() for s in segments)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No video ID or URL provided"}))
        sys.exit(1)

    results = {}
    for arg in sys.argv[1:]:
        vid = extract_video_id(arg)
        if vid:
            transcript = get_transcript(vid)
            results[arg] = transcript
        else:
            results[arg] = "Error: Invalid YouTube URL or ID"
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
