import React from 'react';
// Import the new component
import UploadForm from './pages/UploadForm.jsx'; 
// Assuming you have some basic styling in index.css

function App() {
  return (
    <>
      <header>
        <h1>My React App</h1>
        <nav>
          {/* Add any navigation links here */}
        </nav>
      </header>
      
      <main>
        {/* Render the upload form */}
        <UploadForm />
        
        {/* You can add routing logic here later if needed */}
      </main>
    </>
  );
}

export default App;