// import React, { useRef, useState } from "react";

// const PalmScan = () => {
//   const videoRef = useRef(null);
//   const canvasRef = useRef(null);
//   const [scanning, setScanning] = useState(false);
//   const [message, setMessage] = useState("");

//   const startCamera = async () => {
//     try {
//       const stream = await navigator.mediaDevices.getUserMedia({ video: true });
//       videoRef.current.srcObject = stream;
//     } catch (error) {
//       console.error("Error accessing webcam:", error);
//       setMessage("🚫 Unable to access webcam.");
//     }
//   };

//   const captureImage = () => {
//     const context = canvasRef.current.getContext("2d");
//     context.drawImage(videoRef.current, 0, 0, 224, 224);
//     return canvasRef.current.toDataURL("image/jpeg");
//   };

//   const scanLoop = async () => {
//     setMessage("🔍 Scanning...");
//     setScanning(true);

//     let matchFound = false;

//     for (let i = 0; i < 5; i++) {
//       const image = captureImage();

//       try {
//         const response = await fetch("http://localhost:3001/match_palm", {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({ image }),
//           credentials: "include",
//           mode: "cors",
//         });

//         if (!response.ok) {
//           const text = await response.text();
//           throw new Error(`HTTP ${response.status} - ${text}`);
//         }

//         const data = await response.json();
//         console.log("Match response:", data);

//         // If any response contains match or fallback true, mark as matched
//         if (data.match === true || data.fallback === true) {
//           matchFound = true;
//         }

//       } catch (err) {
//         console.error("Error sending image:", err);
//       }

//       await new Promise((res) => setTimeout(res, 1000)); // Wait between frames
//     }

//     setScanning(false);
//     setMessage(matchFound ? "✅ Palm match successful!" : "❌ No match found.");
//   };

//   const startPalmScan = () => {
//     setMessage("");
//     scanLoop();
//   };

//   return (
//     <div style={{ textAlign: "center" }}>
//       <h2>🖐️ Scan Your Palm</h2>
//       <video
//         ref={videoRef}
//         autoPlay
//         style={{ width: "300px", borderRadius: "12px" }}
//       />
//       <canvas
//         ref={canvasRef}
//         width="224"
//         height="224"
//         style={{ display: "none" }}
//       />
//       <br />
//       <button onClick={startCamera}>Start Camera</button>
//       <button
//         onClick={startPalmScan}
//         disabled={scanning}
//         style={{ marginLeft: "10px" }}
//       >
//         {scanning ? "Scanning..." : "Start Palm Scan"}
//       </button>
//       <p style={{ marginTop: "20px", fontWeight: "bold", fontSize: "18px" }}>
//         {message}
//       </p>
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
  const [amount, setAmount] = useState("");

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    } catch (error) {
      console.error("Error accessing webcam:", error);
      setMessage("🚫 Unable to access webcam.");
    }
  };

  const captureImage = () => {
    const context = canvasRef.current.getContext("2d");
    context.drawImage(videoRef.current, 0, 0, 224, 224);
    return canvasRef.current.toDataURL("image/jpeg");
  };

  const triggerTransaction = async () => {
    try {
      const response = await fetch("http://localhost:3001/receive_money", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount }),
        credentials: "include",
        mode: "cors",
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status} - ${text}`);
      }

      const data = await response.json();
      setMessage(`💸 Transaction successful! ₹${data.transferred}`);
    } catch (err) {
      console.error("Error in transaction:", err);
      setMessage("❌ Transaction failed.");
    }
  };

  const scanLoop = async () => {
    setMessage("🔍 Scanning...");
    setScanning(true);
    let matchFound = false;

    for (let i = 0; i < 5; i++) {
      const image = captureImage();

      try {
        const response = await fetch("http://localhost:3001/match_palm", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image }),
          credentials: "include",
          mode: "cors",
        });

        if (!response.ok) {
          const text = await response.text();
          throw new Error(`HTTP ${response.status} - ${text}`);
        }

        const data = await response.json();
        console.log(`Frame ${i + 1}:`, data);

        if (data.match === true || data.success === true) {
          matchFound = true;
          break;
        }
      } catch (err) {
        console.error("Error sending image:", err);
      }

      setMessage(`🔍 Scanning frame ${i + 1} of 5...`);
      await new Promise((res) => setTimeout(res, 1000));
    }

    setScanning(false);

    if (matchFound) {
      setMessage("✅ Palm match successful! Processing transaction...");
      await triggerTransaction();
    } else {
      setMessage("❌ No match found. Transaction aborted.");
    }
  };

  const handleReceiveMoney = () => {
    if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
      setMessage("⚠️ Enter a valid amount.");
      return;
    }
    setMessage("");
    scanLoop();
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h2>🖐️ Receive Money via Palm Scan</h2>

      <video
        ref={videoRef}
        autoPlay
        style={{ width: "300px", borderRadius: "12px", marginBottom: "10px" }}
      />
      <canvas
        ref={canvasRef}
        width="224"
        height="224"
        style={{ display: "none" }}
      />
      <br />

      <input
        type="number"
        placeholder="Enter amount (₹)"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        style={{
          padding: "8px",
          borderRadius: "8px",
          border: "1px solid #ccc",
          marginBottom: "10px",
        }}
      />
      <br />

      <button
        onClick={startCamera}
        style={{
          padding: "8px 16px",
          borderRadius: "8px",
          backgroundColor: "#007bff",
          color: "#fff",
          border: "none",
        }}
      >
        Start Camera
      </button>

      <button
        onClick={handleReceiveMoney}
        disabled={scanning}
        style={{
          padding: "8px 16px",
          borderRadius: "8px",
          marginLeft: "10px",
          backgroundColor: scanning ? "#ccc" : "#28a745",
          color: "#fff",
          border: "none",
        }}
      >
        {scanning ? "🔄 Scanning..." : "💸 Receive Money"}
      </button>

      <p style={{ marginTop: "20px", fontWeight: "bold", fontSize: "18px" }}>
        {message}
      </p>
    </div>
  );
};

export default PalmScan;
