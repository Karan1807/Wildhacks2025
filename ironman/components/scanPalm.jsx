// import React, { useRef, useState } from "react";
// import Webcam from "react-webcam";

// const PalmScan = () => {
//   const webcamRef = useRef(null);
//   const [result, setResult] = useState(null);
//   const [scanning, setScanning] = useState(false);

//   const scanDuration = 10000; // 10 seconds
//   const interval = 1000; // check every 1 second

//   const startPalmScan = async () => {
//     if (!webcamRef.current) return;
//     setScanning(true);
//     setResult(null);

//     const endTime = Date.now() + scanDuration;
//     let matchFound = false;

//     const scanLoop = async () => {
//       if (!webcamRef.current) return;

//       const imageSrc = webcamRef.current.getScreenshot();

//       const res = await fetch("http://localhost:3001/match_palm", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ image: imageSrc }),
//       });

//       const data = await res.json();

//       if (data.success) {
//         setResult({
//           name: data.user.name,
//           email: data.user.email,
//           id: data.user.id,
//           similarity: data.similarity,
//         });
//         matchFound = true;
//         setScanning(false);
//         return;
//       }

//       if (Date.now() < endTime && !matchFound) {
//         setTimeout(scanLoop, interval); // continue scanning
//       } else {
//         setScanning(false);
//         if (!matchFound) {
//           setResult({ error: "No match found after scanning." });
//         }
//       }
//     };

//     scanLoop();
//   };

//   return (
//     <div style={{ textAlign: "center" }}>
//       <h2>🖐️ Scan Your Palm</h2>
//       <Webcam
//         audio={false}
//         height={300}
//         ref={webcamRef}
//         screenshotFormat="image/jpeg"
//         width={300}
//         videoConstraints={{ facingMode: "user" }}
//       />
//       <br />
//       <button onClick={startPalmScan} disabled={scanning}>
//         {scanning ? "Scanning for 15 seconds..." : "Start Scan"}
//       </button>

//       {result && result.name && (
//         <div style={{ marginTop: "20px" }}>
//           <h3>✅ Match Found!</h3>
//           <p>
//             <strong>ID:</strong> {result.id}
//           </p>
//           <p>
//             <strong>Name:</strong> {result.name}
//           </p>
//           <p>
//             <strong>Email:</strong> {result.email}
//           </p>
//           <p>
//             <strong>Similarity:</strong> {result.similarity.toFixed(4)}
//           </p>
//         </div>
//       )}

//       {result?.error && (
//         <div style={{ marginTop: "20px", color: "red" }}>
//           <h3>❌ {result.error}</h3>
//         </div>
//       )}
//     </div>
//   );
// };

// export default PalmScan;
import React, { useRef, useState } from "react";

const PalmScan = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [scanning, setScanning] = useState(false);
  const [message, setMessage] = useState("");

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    } catch (error) {
      console.error("Error accessing webcam:", error);
    }
  };

  const captureImage = () => {
    const context = canvasRef.current.getContext("2d");
    context.drawImage(videoRef.current, 0, 0, 224, 224); // resize here
    const base64Image = canvasRef.current.toDataURL("image/jpeg");
    return base64Image;
  };

  const sendImage = async (image) => {
    try {
      const response = await fetch("http://localhost:3001/match_palm", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image }),
        credentials: "include",
        mode: "cors",
      });
      if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status} - ${text}`);
      }

      const data = await response.json();
      console.log("Match response:", data);
      setMessage(data.message || (data.match ? "Palm matched!" : "No match."));
    } catch (err) {
      console.error("Error sending image:", err);
      setMessage("Failed to connect to server.");
    }
  };

  const scanLoop = async () => {
    for (let i = 0; i < 5; i++) {
      const image = captureImage();
      await sendImage(image);
      await new Promise((res) => setTimeout(res, 1000));
    }
    setScanning(false);
  };

  const startPalmScan = () => {
    setMessage("");
    setScanning(true);
    scanLoop();
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h2>Scan Your Palm</h2>
      <video
        ref={videoRef}
        autoPlay
        style={{ width: "300px", borderRadius: "12px" }}
      />
      <canvas
        ref={canvasRef}
        width="224"
        height="224"
        style={{ display: "none" }}
      />
      <br />
      <button onClick={startCamera}>Start Camera</button>
      <button
        onClick={startPalmScan}
        disabled={scanning}
        style={{ marginLeft: "10px" }}
      >
        {scanning ? "Scanning..." : "Start Palm Scan"}
      </button>
      <p>{message}</p>
    </div>
  );
};

export default PalmScan;
