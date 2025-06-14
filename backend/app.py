from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Replace with your actual API key
GENAI_API_KEY = "AIzaSyAMtvMu4FkXaBgd5p5F3aEwENKdkX65bU0"
genai.configure(api_key=GENAI_API_KEY)

# Initialize the correct Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')  # Updated model name

def extract_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]  # Handle additional URL parameters
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]  # Handle URL parameters
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

        prompt = f"""Summarize this YouTube video transcript in 3-5 bullet points:
        {transcript_text}"""

        response = model.generate_content(prompt)
        summary = response.text

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)