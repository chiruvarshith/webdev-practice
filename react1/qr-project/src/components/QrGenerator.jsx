import React, { useState, useRef } from 'react';
import QRCode from 'qrcode.react';
import { useReactToPrint } from 'react-to-print';

function QRCodeGenerator() {
  const [id, setId] = useState('');
  const [url, setUrl] = useState('');
  const qrCodeRef = useRef();

  const generateQRCode = () => {
    const websiteUrl = `www.hi/${id}`;
    setUrl(websiteUrl);
  };

  const handlePrint = useReactToPrint({
    content: () => qrCodeRef.current,
  });

  return (
    <div>
      <h1>QR Code Generator</h1>
      <div>
        <input
          type="text"
          placeholder="Enter ID"
          value={id}
          onChange={(e) => setId(e.target.value)}
        />
        <button onClick={generateQRCode}>Generate QR Code</button>
        {url && (
          <button onClick={handlePrint}>Download QR Code</button>
        )}
      </div>
      {url && (
        <div>
          <h2>Generated QR Code:</h2>
          <div ref={qrCodeRef}>
            <QRCode value={url} />
          </div>
        </div>
      )}
    </div>
  );
}

export default QRCodeGenerator;
