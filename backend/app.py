from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Load Gemini API key from environment
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GENAI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set in environment")
genai.configure(api_key=GENAI_API_KEY)

# Use supported Gemini model
model = genai.GenerativeModel("gemini-pro")

def extract_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return url

@app.route("/summarize", methods=["POST"])
def summarize_video():
    try:
        data = request.json
        video_url = data.get("url")
        if not video_url:
            return jsonify({"error": "No URL provided"}), 400

        video_id = extract_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t["text"] for t in transcript])

        prompt = f"""Summarize this YouTube video transcript in 3-5 bullet points:\n\n{transcript_text[:8000]}"""
        response = model.generate_content(prompt)

        summary = getattr(response, "text", "").strip()
        if not summary:
            raise ValueError("Empty summary from Gemini")

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
