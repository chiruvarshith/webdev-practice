// src/ImageProcessor.js
import React, { useRef, useState } from 'react';

const ImageProcessor = () => {
  const [image, setImage] = useState(null);
  const [finalImage, setFinalImage] = useState(null);
  const canvasRef = useRef(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      setImage(reader.result);
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const pixelateImage = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const img = new Image();

    img.onload = () => {
      // Set canvas dimensions to match the image
      canvas.width = img.width;
      canvas.height = img.height;

      // Draw the image onto the canvas
      ctx.drawImage(img, 0, 0);

      // Pixelate the image
      const pixelSize = Math.ceil(img.width / 64);
      const imageData = ctx.getImageData(0, 0, img.width, img.height);
      const data = imageData.data;

      for (let y = 0; y < img.height; y += pixelSize) {
        for (let x = 0; x < img.width; x += pixelSize) {
          const red = data[((img.width * y) + x) * 4];
          const green = data[((img.width * y) + x) * 4 + 1];
          const blue = data[((img.width * y) + x) * 4 + 2];
          const alpha = data[((img.width * y) + x) * 4 + 3];

          ctx.fillStyle = `rgba(${red},${green},${blue},${alpha / 255})`;
          ctx.fillRect(x, y, pixelSize, pixelSize);
        }
      }

      // Convert the canvas content to a data URL and set it as the final image
      setFinalImage(canvas.toDataURL());
    };

    img.src = image;
  };

  return (
    <div className="image-processor">
      <input type="file" accept="image/*" onChange={handleImageChange} />
      <button onClick={pixelateImage}>Convert</button>
      <div className="image-container">
        {finalImage && (
          <img
            src={finalImage}
            alt="Final Result"
          />
        )}
      </div>
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      <style jsx>{`
        .image-processor {
          display: flex;
          flex-direction: column;
          align-items: center;
          margin: 20px;
        }
        .image-container {
          margin-top: 20px;
        }
      `}</style>
    </div>
  );
};

export default ImageProcessor;
