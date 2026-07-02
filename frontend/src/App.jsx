import React, { useState, useRef, useEffect } from 'react';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const [theme, setTheme] = useState('light');

  useEffect(() => {
    document.body.className = theme;
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = (selectedFile) => {
    if (selectedFile.type.startsWith('image/')) {
      setFile(selectedFile);
      setResult(null);
      setError(null);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      alert('Please upload a valid image file.');
    }
  };

  const handlePredict = async () => {
    if (!file) return;

    setIsLoading(true);
    setResult(null);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);

    const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
      ? 'http://localhost:5000/predict' 
      : '/api/predict';

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setResult({
          gesture: data.gesture,
          confidence: (data.confidence * 100).toFixed(1)
        });
      } else {
        setError(data.error || "Failed to analyze image");
      }
    } catch (err) {
      setError("Could not connect to backend server. Is app.py running?");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <button onClick={toggleTheme} className="theme-btn" title="Toggle Theme">
          {theme === 'light' ? <i className="fa-solid fa-moon"></i> : <i className="fa-solid fa-sun"></i>}
        </button>
        <h1><i className="fa-solid fa-hand-sparkles"></i> Hand Gesture Recognition</h1>
        <p>Upload a photo to identify the hand gesture and see how the model reached its decision.</p>
      </header>

      <div className="main-content">
        {/* Left Column */}
        <div className="left-column">
          <div className="input-card">
            <div className="card-header">
              <span>IMAGE INPUT</span>
            </div>
            
            <div className="card-body">
              {!file ? (
                <div 
                  className={`drop-zone ${isDragging ? 'dragover' : ''}`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current.click()}
                >
                  <i className="fa-solid fa-arrow-up-from-bracket upload-icon"></i>
                  <p className="drop-title">Drop image here</p>
                  <p className="drop-subtitle">or click to browse &middot; JPG PNG WebP</p>
                  <input 
                    type="file" 
                    className="file-input" 
                    accept="image/*" 
                    ref={fileInputRef}
                    onChange={handleFileChange}
                  />
                </div>
              ) : (
                <div className="preview-area">
                  <img src={preview} alt="Preview" className="preview-img" />
                  <div className="action-buttons">
                    <button className="btn-primary" onClick={handlePredict} disabled={isLoading}>
                      {isLoading ? 'Analyzing...' : 'Analyze Gesture'}
                    </button>
                    <button className="btn-secondary" onClick={handleReset} disabled={isLoading}>
                      Clear
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="metrics-card">
            <div className="metric-row">
              <span className="metric-label">Training Images</span>
              <span className="metric-value">20,000</span>
            </div>
            <div className="metric-row border-none">
              <span className="metric-label">CNN Architecture</span>
              <span className="metric-value">4-Layer</span>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="right-column">
          <div className="tabs">
            <div className="tab active">Classification</div>
          </div>

          <div className="result-panel">
            {!result && !error && !isLoading && (
              <div className="empty-state">
                <i className="fa-solid fa-paw empty-icon"></i>
                <p>Upload an image and analyze it to see the classification result here.</p>
              </div>
            )}

            {isLoading && (
              <div className="loading-state">
                <div className="spinner"></div>
                <p>Analyzing image structure...</p>
              </div>
            )}

            {(result || error) && (
              <div className="classification-result">
                {error ? (
                  <div className="error-box">
                    <i className="fa-solid fa-triangle-exclamation"></i>
                    <p>{error}</p>
                  </div>
                ) : (
                  <div className="success-box">
                    <h2>{result.gesture}</h2>
                    <div className="confidence-meter">
                      <div className="meter-bg">
                        <div className="meter-fill" style={{width: `${result.confidence}%`}}></div>
                      </div>
                      <p>Confidence: {result.confidence}%</p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
