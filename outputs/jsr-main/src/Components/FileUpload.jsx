import React, { useState } from 'react';

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');
  const [originalImage, setOriginalImage] = useState('');
  const [segmentedImage, setSegmentedImage] = useState('');
  const [pixelCount, setPixelCount] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('Please select a file to upload');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('File upload failed');
      }

      const data = await response.json();
      setOriginalImage(data.original_image);
      setSegmentedImage(data.segmented_image);
      setPixelCount(data.pixel_count);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {originalImage && segmentedImage && (
        <div>
          <h3>Results</h3>
          <p>Segmented Pixels: {pixelCount}</p>
          <img src={`http://127.0.0.1:5000/${originalImage}`} alt="Original" />
          <img src={`http://127.0.0.1:5000/${segmentedImage}`} alt="Segmented" />
        </div>
      )}
    </div>
  );
};

export default FileUpload;
