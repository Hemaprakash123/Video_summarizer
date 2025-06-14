from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/summarize": {
        "origins": ["*"]  # Adjust in production to your frontend URL
    }
})

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')  # Updated to latest model

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:v=|v\/|vi=|vi\/|youtu\.be\/|\/embed\/|\/v\/|\/e\/)([^#\&\?]*).*',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.route("/summarize", methods=["POST"])
def summarize_video():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "No URL provided"}), 400

        video_url = data['url']
        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        # Get transcript
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([t["text"] for t in transcript])
        except NoTranscriptFound:
            return jsonify({
                "error": "No captions available",
                "solution": "Try a different video with captions enabled"
            }), 400

        # Generate summary
        prompt = f"""Create a structured summary with:
        1. 3-5 Key Points
        2. Main Takeaways
        3. Video Length: {len(transcript)} segments
        
        Transcript: {transcript_text}"""
        
        response = model.generate_content(prompt)
        if not response.text:
            raise ValueError("Empty response from Gemini")

        return jsonify({
            "summary": response.text,
            "video_id": video_id,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "error": "Failed to generate summary",
            "details": str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
