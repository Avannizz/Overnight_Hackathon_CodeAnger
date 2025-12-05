import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './UploadForm.css';

const UploadForm = () => {
    const navigate = useNavigate();
    const [inputUser, setInputUser] = useState('');
    const [uploadedHashes, setUploadedHashes] = useState({ 
        sha256: 'Pending...', 
        phash: 'Pending...'
    });
    
    const [selectedFile, setSelectedFile] = useState(null);
    const [message, setMessage] = useState('');
    
    // 💡 NEW STATE: To hold the temporary URL for the image preview
    const [previewUrl, setPreviewUrl] = useState(null); 

    const fileInputRef = useRef(null);

    // --- Handlers ---
    
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        
        setSelectedFile(file);
        setMessage(file ? `File selected: ${file.name}` : 'No file selected');
        
        // 💡 CRITICAL CHANGE: Create and set the preview URL
        if (file) {
            const url = URL.createObjectURL(file);
            setPreviewUrl(url);
        } else {
            setPreviewUrl(null);
        }
    };

    const handleClearMedia = () => {
        setSelectedFile(null);
        setInputUser('');
        setMessage('');
        setUploadedHashes({ sha256: 'Pending...', phash: 'Pending...' }); 
        
        // 💡 Clear and revoke the temporary URL
        if (previewUrl) {
            URL.revokeObjectURL(previewUrl); 
            setPreviewUrl(null);
        }
        
        if (fileInputRef.current) {
            fileInputRef.current.value = ""; 
        }
    };

    // --- (handleButtonClick, handleChange, and handleFileUpload functions are unchanged) ---
    const handleButtonClick = () => {
        fileInputRef.current.click();
    };

    const handleChange = (event) => {
        setInputUser(event.target.value);
    };

    const handleFileUpload = async () => {
        if (!selectedFile) {
            setMessage('Please select a file first!');
            return;
        }
        
        setUploadedHashes({ sha256: 'Calculating...', phash: 'Calculating...' });
        setMessage('Uploading and verifying...');

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('user', inputUser); 

        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                
                setUploadedHashes({
                    sha256: result.sha256_hash,
                    phash: result.phash_hash,
                });
                
                setMessage(`Verification successful! Redirecting...`);
                
                navigate('/result', {
                    state: { 
                        verificationData: result 
                    }
                });
            } else {
                const errorData = await response.json();
                setMessage(`Upload failed: ${errorData.reason || errorData.error || response.statusText}`);
                setUploadedHashes({ sha256: 'Error', phash: 'Error' });
            }
        } catch (error) {
            console.error('Network Error:', error);
            setMessage('An error occurred while connecting to the server.');
            setUploadedHashes({ sha256: 'Network Error', phash: 'Network Error' });
        }
    };

    // --- JSX Return ---
    return (
        <div className="upload-background">
            <div className="upload-form-container">
                <h1>Verify Image Authenticity 📂</h1>
                <p>Select a file from your laptop and click "Upload".</p>
                
                {/* File Upload Button */}
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
                
                {/* Username Input */}
                <div className="upload-user">
                    <div className='user-title'><h2>Enter Orginal User:</h2></div>
                    <input
                        type='text'
                        placeholder='Type Username here!'
                        value={inputUser}
                        onChange={handleChange}
                        className='upload-user-input' 
                        style={{borderRadius:"50px",width:"350px",height:"30px",border:"0px"}}
                    />
                </div>
                
                {/* Digital Fingerprints Display */}
                <div className="upload-fp">
                    <div className='upload-fp-title'><h2>Digital Fingerprints</h2></div>
                    <div className="hashes-u-wrapper">
                        
                        <div className="hash-u-box">
                            <h3 className="hash-u-title">SHA-256</h3>
                            <pre className="hash-u-content">{uploadedHashes.sha256}</pre>
                        </div>

                        <div className="hash-u-box">
                            <h3 className="hash-u-title">P-hash</h3>
                            <pre className="hash-u-content">{uploadedHashes.phash}</pre>
                        </div>
                    </div>
                </div>

                {/* Preview Box - Now displays the image */}
                <div className="upload-prev">
                    {previewUrl ? (
                        <img 
                            src={previewUrl} 
                            alt="Preview of uploaded media" 
                            style={{ 
                                width: '100%', 
                                height: '100%', 
                                objectFit: 'contain', // Ensures image covers the box
                                borderRadius: '30px' // Matches container's radius
                            }} 
                        />
                    ) : (
                        <p style={{ color: 'white', textAlign: 'center', paddingTop: '80px' }}>
                            Image Preview
                        </p>
                    )}
                </div>
            </div>
            
            {/* Action Buttons (Verify/Clear) */}
            <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', width: '100%' }}>
                <div className='upload-verify'>
                    <button className="upload-verify-button" onClick={handleFileUpload}>
                        Start Verification
                    </button>
                </div>
            </div>
            
            {message && 
                <p style={{ marginTop: '20px', textAlign: 'center', color: message.includes('successful') ? 'green' : 'red' }}>
                    {message}
                </p>
            }
        </div>
    );
};

export default UploadForm;