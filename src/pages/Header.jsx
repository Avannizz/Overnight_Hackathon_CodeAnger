import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Header.css';



const Header = () => {

    const navigate = useNavigate();
    const location = useLocation();

    const isActive = (tabName) => {
        const path = `/${tabName.toLowerCase()}`;
        if (tabName === 'Verify') {
            return location.pathname === '/' || location.pathname === '/verify';
        }
        return location.pathname === path;
    };
    
    const navItems = ['Register', 'Verify', 'Help'];

    const handleTabClick = (tabName) => {
        const path = `/${tabName.toLowerCase()}`;
        navigate(path);
    };

    return (
        <header className='header'>
            <div className='header-left'>
                <h1>ContentAuth</h1>
            </div>

            <div className='header-right'>
                {navItems.map((item) => (
                    <div
                        key={item}
                        className={`nav-item ${isActive(item) ? 'active-tab' : ''}`}
                        onClick={() => handleTabClick(item)}
                    >
                        {item}
                        {isActive(item) && <div className='active-indicator'></div>}
                    </div>
                ))}
            </div>
        </header>
    );
}