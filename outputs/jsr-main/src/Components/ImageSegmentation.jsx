import React, { useState, useRef } from "react";

const ImageSegmentation = ({ apiUrl, maxSize = 1024 }) => {
  const [originalImage, setOriginalImage] = useState(null);
  const [segmentedImage, setSegmentedImage] = useState(null);
  const [pixelCount, setPixelCount] = useState(0);
  const fileInputRef = useRef(null);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const img = new Image();
    img.src = URL.createObjectURL(file);

    img.onload = async () => {
      let { width, height } = img;
      let canvas = document.createElement("canvas");
      let context = canvas.getContext("2d");

      // Resize the image if needed
      if (Math.max(width, height) > maxSize) {
        if (width > height) {
          const ratio = maxSize / width;
          width = maxSize;
          height = height * ratio;
        } else {
          const ratio = maxSize / height;
          height = maxSize;
          width = width * ratio;
        }
      }

      canvas.width = width;
      canvas.height = height;
      context.drawImage(img, 0, 0, width, height);
      const resizedImage = canvas.toDataURL();

      setOriginalImage(resizedImage);

      // Send image to API
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch(apiUrl, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`Failed to get predictions: ${response.status}`);
        }

        const { predictions } = await response.json();

        // Draw segmentation overlay
        const overlayCanvas = document.createElement("canvas");
        const overlayContext = overlayCanvas.getContext("2d");
        overlayCanvas.width = width;
        overlayCanvas.height = height;

        predictions.forEach((prediction) => {
          const points = prediction.points || [];
          if (points.length) {
            overlayContext.beginPath();
            overlayContext.moveTo(points[0].x, points[0].y);
            points.forEach(({ x, y }) => overlayContext.lineTo(x, y));
            overlayContext.closePath();
            overlayContext.fillStyle = "rgba(255, 0, 0, 0.4)";
            overlayContext.fill();
          }
        });

        // Combine original and overlay
        context.globalCompositeOperation = "source-over";
        context.drawImage(overlayCanvas, 0, 0);

        const combinedImage = canvas.toDataURL();
        setSegmentedImage(combinedImage);

        // Count segmented pixels
        const maskData = overlayContext.getImageData(0, 0, width, height).data;
        const pixelCount = maskData.reduce(
          (count, value, index) => count + (index % 4 === 3 && value > 0 ? 1 : 0),
          0
        );
        setPixelCount(pixelCount);
      } catch (error) {
        console.error(error.message);
      }
    };
  };

  return (
    <div>
      <h1>Image Segmentation</h1>
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        onChange={handleImageUpload}
      />
      {originalImage && (
        <div>
          <h2>Original Image</h2>
          <img src={originalImage} alt="Original" />
        </div>
      )}
      {segmentedImage && (
        <div>
          <h2>Segmented Image</h2>
          <img src={segmentedImage} alt="Segmented" />
          <p>Segmented Pixel Count: {pixelCount}</p>
        </div>
      )}
    </div>
  );
};

export default ImageSegmentation;
