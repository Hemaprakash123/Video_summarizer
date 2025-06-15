📺 YouTube Video Summarizer AI
An AI-powered web application that summarizes YouTube videos using Google Gemini and YouTube transcripts.

Screenshot:
![Screenshot (62)](https://github.com/user-attachments/assets/ae100096-9fa5-4e65-b092-1f66c2f56935)


🚀 Features
🎥 Extracts transcript from YouTube videos

🧠 Uses Google Gemini (Generative AI) to generate summaries

⚡ Clean, responsive frontend built with React

🔐 Backend built with Flask & deployed to Render

✂️ Returns 3–5 bullet-point summaries

| Frontend   | Backend        | AI Service   |
| ---------- | -------------- | ------------ |
| React      | Flask (Python) | Gemini API   |
| CSS / HTML | Flask-CORS     | Google GenAI | 


🛠️ Setup Instructions
🧩 Prerequisites
Node.js & npm

Python 3.8+

A Google Gemini API Key (from makersuite.google.com)

🔧 Backend (Flask)
1. Clone the repository
git clone https://github.com/yourusername/video-summarizer.git
cd video-summarizer/backend

2. Create virtual environment and install packages

python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Create .env file
GEMINI_API_KEY=your_actual_google_genai_api_key

4. Run the backend
bash
Copy
Edit
python app.py
It will start on: http://localhost:5000

🎨 Frontend (React)
1. Navigate to frontend folder

cd ../frontend
2. Install packages

npm install
3. Start frontend

npm start
Frontend runs on http://localhost:3000 and sends POST requests to http://localhost:5000/summarize.



🙋‍♂️ Created By
Hema Prakash
Frontend & Backend Developer
📧 Email: hemaprakashreddy73@gmail.com


