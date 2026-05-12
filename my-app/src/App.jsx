// src/App.jsx
import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [matches, setMatches] = useState([]);      // errors from LanguageTool
  const [hoveredIndex, setHoveredIndex] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  const checkGrammar = async () => {
    if (!text.trim()) {
      setMatches([]);
      setApiError("Type something first.");
      return;
    }

    setLoading(true);
    setApiError("");
    setHoveredIndex(null);

    try {
      const res = await fetch("https://api.languagetool.org/v2/check", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `text=${encodeURIComponent(text)}&language=en-US`,
      });

      const data = await res.json();
      setMatches(data.matches || []);
    } catch (err) {
      console.error(err);
      setApiError("Something went wrong while checking.");
      setMatches([]);
    } finally {
      setLoading(false);
    }
  };

  // Build highlighted text from `text` + `matches`
  const renderHighlightedText = () => {
    if (!text) {
      return <span className="muted">Your checked text will appear here.</span>;
    }

    if (!matches.length) {
      // no errors → just show plain text
      return <span>{text}</span>;
    }

    const sorted = [...matches].sort((a, b) => a.offset - b.offset);
    const parts = [];
    let lastIndex = 0;

    sorted.forEach((m, i) => {
      const start = m.offset;
      const end = m.offset + m.length;

      // normal text before the error
      if (start > lastIndex) {
        parts.push(
          <span key={`t-${i}-${lastIndex}`}>{text.slice(lastIndex, start)}</span>
        );
      }

      // error span
      parts.push(
        <span
          key={`e-${i}-${start}`}
          className="error-span"
          onMouseEnter={() => setHoveredIndex(i)}
          onMouseLeave={() => setHoveredIndex(null)}
        >
          {text.slice(start, end)}
        </span>
      );

      lastIndex = end;
    });

    // remaining text after last error
    if (lastIndex < text.length) {
      parts.push(
        <span key={`t-end-${lastIndex}`}>{text.slice(lastIndex)}</span>
      );
    }

    return parts;
  };

  const hoveredMatch =
    hoveredIndex !== null ? matches[hoveredIndex] : null;

  return (
    <div className="app-root">
      <h1>Grammie</h1>
      <p className="subtitle">
        Type some text, click <strong>Check</strong>, then hover red words to see suggestions.
      </p>

      <textarea
        className="input-area"
        placeholder="Enter your message here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        className="check-btn"
        onClick={checkGrammar}
        disabled={loading}
      >
        {loading ? "Checking..." : "Check Grammar"}
      </button>

      {apiError && <div className="error-banner">{apiError}</div>}

      <div className="output-box">
        {renderHighlightedText()}
      </div>

      {hoveredMatch && (
        <div className="popup">
          <div className="popup-title">Issue</div>
          <div className="popup-message">{hoveredMatch.message}</div>

          <div className="popup-subtitle">Suggestions</div>
          <div className="popup-suggestions">
            {hoveredMatch.replacements && hoveredMatch.replacements.length ? (
              hoveredMatch.replacements.map((r, i) => (
                <div key={i} className="popup-option">
                  {r.value}
                </div>
              ))
            ) : (
              <div className="popup-option muted">
                No suggestions available.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

