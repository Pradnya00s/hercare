import { useState } from "react";
import axios from "axios";
import "./UltrasoundUpload.css";

/**
 * UltrasoundUpload Component
 * ===========================
 * Allows users to upload ultrasound images for CNN-based PCOS prediction.
 * 
 * Props:
 * - symptomResult: Symptom prediction result from previous stage
 * - onUploadSuccess: Callback when prediction is successful
 * - onCancel: Callback to return to previous stage
 */
function UltrasoundUpload({ symptomResult, onUploadSuccess, onCancel }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  // Handle file selection
  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    const allowedTypes = ["image/jpeg", "image/png", "image/gif", "image/bmp"];
    if (!allowedTypes.includes(file.type)) {
      setError("Please select a valid image file (JPEG, PNG, GIF, or BMP)");
      return;
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      setError("File size must be less than 10MB");
      return;
    }

    setSelectedFile(file);
    setError(null);

    // Create preview
    const reader = new FileReader();
    reader.onload = (event) => {
      setPreview(event.target.result);
    };
    reader.readAsDataURL(file);
  };

  // Handle drag and drop
  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add("drag-over");
  };

  const handleDragLeave = (e) => {
    e.currentTarget.classList.remove("drag-over");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove("drag-over");
    
    const file = e.dataTransfer.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError(null);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (event) => {
        setPreview(event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Handle form submission
  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      setError("Please select an image file");
      return;
    }

    setLoading(true);
    setError(null);
    setUploadProgress(0);

    try {
      // Create FormData for multipart file upload
      const formData = new FormData();
      formData.append("ultrasound_image", selectedFile);

      // Upload file to backend
      const response = await axios.post(
        "http://127.0.0.1:8000/api/ultrasound/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          onUploadProgress: (progressEvent) => {
            const progress = Math.round(
              (progressEvent.loaded / progressEvent.total) * 100
            );
            setUploadProgress(progress);
          },
        }
      );

      // Check if upload was successful
      if (response.data.success === false) {
        throw new Error(response.data.error || "Upload failed");
      }

      // Pass result back to parent
      onUploadSuccess(response.data);
    } catch (err) {
      setError(
        err.response?.data?.error || 
        err.message || 
        "Failed to upload image"
      );
      console.error(err);
    } finally {
      setLoading(false);
      setUploadProgress(0);
    }
  };

  // Clear selection
  const handleClear = () => {
    setSelectedFile(null);
    setPreview(null);
    setError(null);
    setUploadProgress(0);
  };

  return (
    <div className="result-card">
      <div className="result-section">
        <h2>📷 Ultrasound Image Analysis</h2>
        
        {symptomResult && (
          <div className="info-box">
            <p>
              <strong>Symptom Assessment:</strong> Your PCOS risk from symptoms is{" "}
              <strong>{symptomResult.pcos_probability.toFixed(1)}%</strong>
            </p>
            <p>
              Now let's enhance accuracy by analyzing an ultrasound image for PCOS indicators.
            </p>
          </div>
        )}
      </div>

      <form onSubmit={handleUpload} className="symptom-form">
        {/* File Upload Area */}
        <div
          className="upload-area"
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {!preview ? (
            <div className="upload-placeholder">
              <div className="upload-icon">📁</div>
              <h3>Drag & Drop Ultrasound Image</h3>
              <p>or click to select from your device</p>
              <p className="upload-info">
                Supported: JPEG, PNG, GIF, BMP (Max 10MB)
              </p>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                disabled={loading}
                style={{ display: "none" }}
                id="file-input"
              />
              <button 
                type="button"
                onClick={() => document.getElementById("file-input").click()}
                disabled={loading}
                className="button-primary"
              >
                Select Image
              </button>
            </div>
          ) : (
            <div className="image-preview">
              <img src={preview} alt="Ultrasound preview" />
              <div className="preview-info">
                <p><strong>File:</strong> {selectedFile.name}</p>
                <p><strong>Size:</strong> {(selectedFile.size / 1024).toFixed(2)} KB</p>
              </div>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && <div className="error-message">⚠️ {error}</div>}

        {/* Upload Progress */}
        {loading && uploadProgress > 0 && (
          <div className="progress-container">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p className="progress-text">{uploadProgress}% Uploading...</p>
          </div>
        )}

        {/* Buttons */}
        <div className="form-actions">
          {selectedFile && (
            <button
              type="submit"
              disabled={loading}
              className="button-primary"
            >
              {loading ? "⏳ Analyzing..." : "📊 Analyze Image"}
            </button>
          )}
          {selectedFile && (
            <button
              type="button"
              onClick={handleClear}
              disabled={loading}
              className="button-secondary"
            >
              Clear
            </button>
          )}
        </div>
      </form>

      {/* Info Section */}
      <div className="info-box" style={{ marginTop: "2rem" }}>
        <p>
          <strong>💡 How it works:</strong> Our CNN model analyzes ultrasound images for ovarian morphology 
          features typical of PCOS. Results are combined with your symptom assessment for comprehensive diagnosis.
        </p>
        <p style={{ fontSize: "0.9rem", marginTop: "1rem", opacity: 0.8 }}>
          This tool is for screening purposes and not a replacement for medical consultation.
        </p>
      </div>
    </div>
  );
}

export default UltrasoundUpload;
