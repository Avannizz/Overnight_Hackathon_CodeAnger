import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './pages/Header.jsx';
import UploadForm from './pages/UploadForm.jsx';
import Register from './pages/Register.jsx'; 
import Help from './pages/Help.jsx';
import Result from './pages/Result.jsx';
import './index.css';

function App() {
  return (
    <> 
      <Header /> 
      
      <main>
        <Routes>
          <Route path="/" element={<UploadForm />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify" element={<UploadForm />} />           
          <Route path="/help" element={<Help />} />
          <Route path="/result" element={<Result />} />
        </Routes>
      </main>
    </>
  );
}

export default App;