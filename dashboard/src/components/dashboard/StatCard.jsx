import React from 'react';
import '../../styles/dashboard.css';

const StatCard = ({ icon, label, value, color, isAlert, isActive = false }) => {
    return (
        <div
            className={`stat-card ${isAlert ? 'alert-card' : ''} ${isActive ? 'active-glow' : ''}`}
            style={{ color: isActive ? color : 'inherit' }}
        >
            <div className="stat-icon" style={{ color: color }}>
                {icon}
            </div>
            <div className="stat-content">
                <span className="stat-label">{label}</span>
                <span className="stat-value">{value}</span>
            </div>
        </div>
    );
};

export default StatCard;
