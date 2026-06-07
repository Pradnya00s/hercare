import React, { useState } from "react";
import "./UploadBox.css";

const UploadBox = ({ onFileSelect }) => {
  const [fileName, setFileName] = useState("");
  const [preview, setPreview] = useState(null);
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

    const file = e.dataTransfer.files[0];
    if (file) {
      setFileName(file.name);
      onFileSelect(file);

      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    }
  };


  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      onFileSelect(file);

      // preview image
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <label className={`upload-box-modern ${dragActive ? "dragging" : ""}`}
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}>
      <input
        type="file"
        accept="image/png, image/jpeg"
        onChange={handleChange}
        hidden
      />

      {preview ? (
        <img src={preview} alt="preview" className="upload-preview" />
      ) : (
        <>
          <div className="upload-icon-modern">
            <i className="ph ph-upload-simple"></i>
          </div>
          <h4>Select file to upload</h4>
          <p>Supports JPG and PNG images</p>
        </>
      )}

      {fileName && <span className="file-name">{fileName}</span>}
    </label>
  );
};

export default UploadBox;