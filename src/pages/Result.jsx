import React from 'react';
import './Result.css';

// NOTE: In a real app, 'results' would be passed as props after the backend returns data.
const mockResults = {
    sha256: 'MATCHED', // or 'NOT MATCHED'
    pHashSimilarity: '98.5%', // e.g., '10%', '98.5%'
    flag: 'NOT COPYRIGHTED', // or 'COPYRIGHTED'
    digitalFingerprints: {
        sha256: 'b4c9e1f3a2dd8b7c6e5f4a3b2c1d0e9f1a7b6c5c5d4e3f\n2a1b0c5d9e7f16a5b4c3d2',
        pHash: 'b4c9e1f3a2dd8b7c6e5f4a3b2c1d0e9f1a7b6c5c5d4e3f\n2a1b0c5d9e7f16a5b4c3d2'
    }
};

const Result = () => {
    const results = mockResults;

    return (
        <div className="result-background">
            <div className="result-form-container">
                
                {/* 1. Verification Result Header */}
                <h1 className="result-title">Verification Result</h1>
                <p className="result-subtitle">Verification for the content posted</p>

                {/* 2. Verification Status Block */}
                <div className="result-verify result-status-box">
                    <div className="status-grid">
                        <div className="result-row">
                            <span className="result-label">SHA-256 :</span>
                            <span className="result-value">{results.sha256}</span>
                        </div>
                        <div className="result-row">
                            <span className="result-label">P-HASH :</span>
                            <span className="result-value similarity-value">{results.pHashSimilarity}</span>
                        </div>
                        <div className="result-row">
                            <span className="result-label">FLAG :</span>
                            <span className="result-value flag-value">{results.flag}</span>
                        </div>
                    </div>
                </div>
                <div  className="fingerprints-title"><h2>Digital Fingerprints</h2></div>
                <div className="result-fp result-fingerprints-box">
                    

                    <div className="hashes-wrapper">
                        <div className="hash-box">
                            <h3 className="hash-title">SHA-256</h3>
                            <pre className="hash-content">{results.digitalFingerprints.sha256}</pre>
                        </div>

                        <div className="hash-box">
                            <h3 className="hash-title">P-hash</h3>
                            <pre className="hash-content">{results.digitalFingerprints.pHash}</pre>
                        </div>
                    </div>
                </div>

                <div className="download-wrapper">
                    <button className="download-button">Download</button>
                </div>
            </div>
        </div>
    );
};

export default Result;