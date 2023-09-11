import React, { useState, useRef, useEffect } from 'react';
import QRCode from 'qrcode.react';
import { useReactToPrint } from 'react-to-print';

function QRCodeGenerator({ id }) {
  const [url, setUrl] = useState(`https://zoopark.vercel.app/${id}`);
  const qrCodeRef = useRef();

  useEffect(() => {
    // Generate QR code when the component is mounted or when the 'id' prop changes
    setUrl(`https://zoopark.vercel.app/${id}`);
  }, [id]);

  const handlePrint = useReactToPrint({
    content: () => qrCodeRef.current,
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center',  height: '100vh' }}>
         <div>
        <button onClick={handlePrint}>Download QR Code</button>
      </div>
      <div>
        <h2>Generated QR Code:</h2>
        <div ref={qrCodeRef}>
          <QRCode value={url} style={{height:"300px" , width:"300px"}}/>
        </div>
      </div>
    </div>
  );
}

export default QRCodeGenerator;
