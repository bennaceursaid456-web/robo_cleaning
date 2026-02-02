import React from 'react';
import '../../styles/dashboard.css';

const DashboardLayout = ({ children }) => {
    return (
        <div className="dashboard-container">
            {/* Header Area */}
            <header className="app-header">
                <div className="brand">
                    <div className="brand-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="18" height="18">
                            <path d="M12 2.69l5.71 5.829a2 2 0 0 0 0 2.828l-5.71 5.816a2 2 0 0 0 0 2.828L12 22" />
                            <path d="M12 2.69l-5.71 5.829a2 2 0 0 1 0 2.828l5.71 5.816a2 2 0 0 1 0 2.828L12 22" />
                        </svg>
                    </div>
                    <div className="brand-text">
                        <h1>AquaMind</h1>
                        <span>AUTONOMOUS WATER CLEANING INTELLIGENCE</span>
                    </div>
                </div>

                <div className="top-status">
                    <div className="status-badge">
                        <div className="pulse"></div>
                        PAUSED • HUMAN DETECTED
                    </div>
                    <div style={{ fontFamily: 'monospace', opacity: 0.5 }}>
                        15:35:59
                    </div>
                </div>
            </header>

            {/* Main Content (Grid Items will be injected here) */}
            {children}
        </div>
    );
};

export default DashboardLayout;
