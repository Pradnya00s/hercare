import React, { useRef, useState } from "react";
import "./UploadBox.css";

const UploadBox = ({ onFileSelect }) => {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  return (
    <div
      className={`upload-box-modern ${dragActive ? "dragging" : ""}`}
      onClick={() => fileInputRef.current.click()}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        ref={fileInputRef}
        accept="image/*"
        onChange={(e) => onFileSelect(e.target.files[0])}
        style={{ display: "none" }}
      />
      
      <div className="upload-icon-modern">
        <i className="ph ph-upload-simple"></i>
      </div>
      <h4>Select file to upload</h4>
      <p>Supports standard medical image formats</p>
    </div>
  );
};

export default UploadBox;