import React, { useState,useRef } from 'react';
import './UploadForm.css'

const mockResults = {
    sha256: 'MATCHED', // or 'NOT MATCHED'
    pHashSimilarity: '98.5%', // e.g., '10%', '98.5%'
    flag: 'NOT COPYRIGHTED', // or 'COPYRIGHTED'
    digitalFingerprints: {
        sha256: 'b4c9e1f3a2dd8b7c6e5f4a3b2c1d0e9f1a7b6c5c5d4e3f\n2a1b0c5d9e7f16a5b4c3d2',
        pHash: 'b4c9e1f3a2dd8b7c6e5f4a3b2c1d0e9f1a7b6c5c5d4e3f\n2a1b0c5d9e7f16a5b4c3d2'
    }
};

const UploadForm = () => {
  const [inputUser, setInputUser] = useState('');
  const results  = mockResults ;
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const fileInputRef = useRef(null);
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setMessage(file ? `File selected: ${file.name}` : 'No file selected');
  };
  const handleButtonClick = () => {
        fileInputRef.current.click();
    };
  const handleChange=(event)=>{
    setInputUser(event.target.value);
  };
  const handleFileUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setMessage(`Upload successful! Hash: ${result.sha256_hash}`);
        setSelectedFile(null); // Clear the selected file after success
      } else {
        const errorData = await response.json();
        setMessage(`Upload failed: ${errorData.error || response.statusText}`);
      }
    } catch (error) {
      console.error('Network Error:', error);
      setMessage('An error occurred while connecting to the server.');
    }
  };

  return (
    <div className="upload-background">
      <div className="upload-form-container">
        <h1>Verify Image Authenticity 📂</h1>
        <p>Select a file from your laptop and click "Upload".</p>
        <div className="upload-button" onClick={handleButtonClick}>
            <input 
            type="file" 
            ref={fileInputRef}
            onChange={handleFileChange} 
            style={{display:'none' }}
            />
            <span className="upload-prompt">
                {selectedFile ? `File Selected: ${selectedFile.name}` : "Click here to choose a file"}
            </span>
            
            <button 
            onClick={handleFileUpload} 
            disabled={!selectedFile}
            className="post-upload-button"
            >
            Upload File
            </button>
        </div>
        <div className="upload-user">
            <div className='user-title'><h2>Enter Orginal User:</h2></div>
            <input
            type='text'
            placeholder='Type Username here!'
            value={inputUser}
            onChange={handleChange}
            display="none"
            style={{borderRadius:"50px",width:"350px",height:"30px",border:"0px"}}
            />

        </div>
        
        <div className="upload-fp">
            <div className='upload-fp-title'><h2>Digital Fingerprints</h2></div>
            <div className="hashes-u-wrapper">
                <div className="hash-u-box">
                    <h3 className="hash-u-title">SHA-256</h3>
                    <pre className="hash-u-content">{results.digitalFingerprints.sha256}</pre>
                </div>

                <div className="hash-u-box">
                    <h3 className="hash-u-title">P-hash</h3>
                    <pre className="hash-u-content">{results.digitalFingerprints.pHash}</pre>
                </div>
            </div>
        
        </div>

        <div className="upload-prev">

        </div>
        
      </div>
      <div className='upload-verify'>
        <button 
            className="upload-verify-button"
        >
            Start Verification
        </button>
      </div>
      <div className='upload-clear'>
        <button 
            className="upload-clear-button"
        >
            Clear Media
        </button>
      </div>
    </div>
  );
};

export default UploadForm;