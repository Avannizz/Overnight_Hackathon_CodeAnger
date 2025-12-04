import React, { useState } from 'react';

const UploadForm = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setMessage(file ? `File selected: ${file.name}` : 'No file selected');
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // NOTE: You must update the URL to match the endpoint in your upload_media.py backend
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setMessage(`Upload successful! ${result.message}`);
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
    <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto' }}>
      <h2>Media Upload 📂</h2>
      <p>Select a file from your laptop and click "Upload".</p>

      {/* Input for selecting the file */}
      <input 
        type="file" 
        onChange={handleFileChange} 
        style={{ margin: '10px 0' }}
      />
      
      {/* Button to trigger the upload */}
      <button 
        onClick={handleFileUpload} 
        disabled={!selectedFile}
        style={{ 
          padding: '10px 20px', 
          backgroundColor: selectedFile ? '#4CAF50' : '#cccccc',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: selectedFile ? 'pointer' : 'not-allowed'
        }}
      >
        Upload File
      </button>

      {/* Display user feedback message */}
      {message && 
        <p style={{ marginTop: '20px', color: message.includes('success') ? 'green' : 'red' }}>
          {message}
        </p>
      }
    </div>
  );
};

export default UploadForm;