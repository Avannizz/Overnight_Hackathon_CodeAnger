import React from 'react';
import { useLocation } from 'react-router-dom'; // 💡 Import useLocation
import './Result.css';

// Remove the mockResults object entirely

const Result = () => {
    // 💡 1. Get data passed during navigation (from UploadForm.jsx)
    const location = useLocation();
    const verificationData = location.state?.verificationData;
    
    // 💡 2. Define data structure for display. Use defaults if navigation data is missing.
    const results = verificationData ? {
        // --- Status Fields (Directly from backend response) ---
        status: verificationData.status,                 // e.g., "registered" or "rejected"
        reason: verificationData.reason || "N/A",       // Only present if rejected
        owner: verificationData.owner,                  // Original owner
        
        // --- Flag/Similarity (Mocked logic, as backend currently returns only hashes) ---
        // NOTE: You need to implement logic in server.py to determine pHashSimilarity and flag.
        // For now, we'll determine flag based on status:
        flag: verificationData.status === 'registered' ? 'NOT COPYRIGHTED' : 'POSSIBLE DUPLICATE',
        pHashSimilarity: '99.9%', // Placeholder until backend is updated for similarity score
        
        // --- Digital Fingerprints (Actual hashes returned) ---
        digitalFingerprints: {
            // Backend returns full strings; use them directly
            sha256: verificationData.sha256_hash,
            pHash: verificationData.phash_hash
        }
    } : null; // Set to null if no data is found

    // Handle case where no data was passed (e.g., user navigated directly)
    if (!results) {
        return (
            <div className="result-background">
                <div className="result-form-container">
                    <h1 className="result-title">Error</h1>
                    <p className="result-subtitle">No verification data found. Please upload a file first.</p>
                </div>
            </div>
        );
    }

    // Determine the main result status text
    const mainStatus = results.status === 'registered' ? 'ACCEPTED (Registered)' : 'REJECTED';
    const statusColor = results.status === 'registered' ? 'green-status' : 'red-status';

    return (
        <div className="result-background">
            <div className="result-form-container">
                
                <h1 className="result-title">Verification Result</h1>
                <p className="result-subtitle">Verification for the content posted</p>

                {/* 2. Verification Status Block (REPLACING MOCK DATA) */}
                <div className={`result-verify result-status-box ${statusColor}`}>
                    <div className="status-grid">
                        
                        {/* MAIN STATUS: ACCEPTED / REJECTED */}
                        <div className="result-row">
                            <span className="result-label">STATUS :</span>
                            <span className={`result-value ${statusColor}`}>{mainStatus}</span>
                        </div>
                        
                        {/* REASON (Only show if rejected) */}
                        {results.status === 'rejected' && (
                            <div className="result-row">
                                <span className="result-label">REASON :</span>
                                <span className="result-value red-status">{results.reason}</span>
                            </div>
                        )}
                        
                        {/* P-HASH SIMILARITY */}
                        <div className="result-row">
                            <span className="result-label">P-HASH SIMILARITY :</span>
                            <span className="result-value similarity-value">{results.pHashSimilarity}</span>
                        </div>
                        
                        {/* FLAG */}
                        <div className="result-row">
                            <span className="result-label">FLAG :</span>
                            <span className="result-value flag-value">{results.flag}</span>
                        </div>
                        
                    </div>
                </div>
                
                <div className="fingerprints-title"><h2>Digital Fingerprints</h2></div>
                <div className="result-fp result-fingerprints-box">
                    
                    <div className="hashes-wrapper">
                        {/* SHA-256 HASH (ACTUAL DATA) */}
                        <div className="hash-box">
                            <h3 className="hash-title">SHA-256</h3>
                            <pre className="hash-content">{results.digitalFingerprints.sha256}</pre>
                        </div>

                        {/* P-HASH (ACTUAL DATA) */}
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