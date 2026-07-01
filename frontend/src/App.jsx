import React, { useState, useRef } from 'react';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

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

    // Dynamic API URL for Vercel deployment
    const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
      ? 'http://localhost:5000/predict' 
      : '/api/predict'; // Adjust based on your Vercel functions setup

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
    <>
      <div className="bg-mesh"></div>
      <div className="container">
        <div className="header">
          <h1>NeuroHand</h1>
          <p>Advanced CNN Gesture Recognition</p>
        </div>

        <div className="glass-card">
          {!file && (
            <div 
              className={`upload-area ${isDragging ? 'dragover' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current.click()}
            >
              <i className="fa-solid fa-cloud-arrow-up upload-icon"></i>
              <h3>Upload an Image</h3>
              <p>Drag & drop or click to browse</p>
              <input 
                type="file" 
                className="file-input" 
                accept="image/*" 
                ref={fileInputRef}
                onChange={handleFileChange}
              />
            </div>
          )}

          {file && !result && !error && !isLoading && (
            <div className="preview-container">
              <img className="preview-image" src={preview} alt="Selected" />
              <button className="btn" onClick={handlePredict}>
                <i className="fa-solid fa-wand-magic-sparkles"></i> Analyze Gesture
              </button>
            </div>
          )}

          {isLoading && (
            <div className="loader"></div>
          )}

          {(result || error) && (
            <div className="results-section" style={{ display: 'block' }}>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '2px' }}>
                Detected Gesture
              </p>
              
              <div className={`prediction-result ${error ? 'error' : ''}`}>
                {error ? 'Error' : result.gesture}
              </div>
              
              <div className="confidence-wrapper">
                <div 
                  className={`confidence-bar ${error ? 'error' : ''}`} 
                  style={{ width: error ? '100%' : `${result.confidence}%` }}
                ></div>
              </div>
              
              <div className="confidence-text">
                {error ? '' : `Confidence: ${result.confidence}%`}
              </div>
              
              {error && (
                <div className="error-text">{error}</div>
              )}

              <button className="reset-btn" onClick={handleReset}>
                <i className="fa-solid fa-rotate-right"></i> Try Another
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default App;
