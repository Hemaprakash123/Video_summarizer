import { useState } from "react";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) {
      setError("Please enter a YouTube URL");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const response = await fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      if (response.ok) {
        setSummary(data.summary);
      } else {
        setError(data.error || "Failed to get summary");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo-container">
          <i className="fab fa-youtube logo-icon"></i>
          <h1 className="title">YouTube Summarizer AI</h1>
        </div>
        <p className="subtitle">Get instant AI-powered summaries of any YouTube video</p>
      </header>

      <main className="main-content">
        <form onSubmit={handleSubmit} className="url-form">
          <div className="input-group">
            <input
              type="text"
              placeholder="Paste YouTube video URL here..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="url-input"
            />
            <button 
              type="submit" 
              disabled={loading} 
              className={`submit-btn ${loading ? 'loading' : ''}`}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Processing...
                </>
              ) : (
                <>
                  <i className="fas fa-magic"></i> Summarize
                </>
              )}
            </button>
          </div>
          {error && <p className="error-message">{error}</p>}
        </form>

        {summary && (
          <div className="summary-container">
            <div className="summary-header">
              <h2>Your Video Summary</h2>
              <div className="summary-actions">
                <button className="copy-btn" onClick={() => navigator.clipboard.writeText(summary)}>
                  <i className="fas fa-copy"></i> Copy
                </button>
              </div>
            </div>
            <div className="summary-content">
              {summary.split('\n').map((paragraph, i) => (
                <p key={i}>{paragraph}</p>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Created By Hema prakash</p>
      </footer>
    </div>
  );
}

export default App;