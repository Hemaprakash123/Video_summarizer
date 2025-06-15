import os
import re
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import google.generativeai as genai
from dotenv import load_dotenv

# Initialize
load_dotenv()
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Gemini setup
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    logging.error(f"Gemini initialization failed: {str(e)}")
    raise

def extract_video_id(url):
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:v=|v/|vi=|vi/|youtu\.be/|/embed/|/v/|/e/)([^#&?]*)',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.route("/summarize", methods=["POST"])
def summarize_video():
    start_time = datetime.now()

    try:
        data = request.get_json()
        if not data or 'url' not in data:
            raise ValueError("Missing YouTube URL")

        video_url = data['url']
        video_id = extract_video_id(video_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL format")

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            transcript_text = " ".join([t['text'] for t in transcript])
        except NoTranscriptFound:
            return jsonify({
                "error": "No English captions available",
                "solution": "Try a video with closed captions"
            }), 400

        prompt = f"""Create a structured summary with:
1. Key Points (3-5 bullet points)
2. Main Takeaways
3. Recommended Audience

Video Transcript: {transcript_text[:8000]}... [truncated if too long]"""

        response = model.generate_content(prompt)

        if not hasattr(response, "text") or not response.text:
            raise ValueError("Empty or invalid response from Gemini API")

        processing_time = (datetime.now() - start_time).total_seconds()
        logging.info(f"Processed video {video_id} in {processing_time:.2f}s")

        return jsonify({
            "summary": response.text,
            "video_id": video_id,
            "processing_time": f"{processing_time:.2f}s"
        })

    except Exception as e:
        logging.exception(f"Error processing {data.get('url', '')}:")
        return jsonify({
            "error": "Failed to generate summary",
            "details": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
