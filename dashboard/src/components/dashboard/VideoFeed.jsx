import React from 'react';
import '../../styles/dashboard.css';
import { api } from '../../services/api';

const VideoFeed = ({ activeCategories = [] }) => {
    // Determine glow class priority: Toxic > Recyclable
    let glowClass = '';
    if (activeCategories.includes('toxic')) {
        glowClass = 'cat-toxic';
    } else if (activeCategories.includes('recyclable')) {
        glowClass = 'cat-recyclable';
    }

    return (
        <div className={`main-feed ${glowClass}`}>
            {/* Live Video Feed */}
            <img
                src={api.videoStreamUrl}
                alt="Live Feed"
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />

            <div className="video-overlay">
                {/* Corner Reticles */}
                <div className="reticle-corner top-left"></div>
                <div className="reticle-corner top-right"></div>
                <div className="reticle-corner bottom-left"></div>
                <div className="reticle-corner bottom-right"></div>

                <div className="feed-status">
                    {/* Center Alert is now handled by the image overlay from backend (drawing boxes) */}
                    {/* But we can keep a "LIVE" indicator */}
                    <div style={{
                        marginTop: '10px',
                        fontSize: '0.8rem',
                        color: '#00ff88',
                        background: 'rgba(0, 255, 136, 0.1)',
                        padding: '4px 12px',
                        borderRadius: '12px',
                        display: 'inline-block'
                    }}>
                        ● LIVE FEED
                    </div>
                </div>

                {/* Bottom Info Bar */}
                <div className="cam-info">
                    <span>CAM-01 • 1920x1080 • MJPEG</span>
                    <span>LAT: 52.5200° N  LON: 13.4050° E</span>
                </div>
            </div>
        </div>
    );
};

export default VideoFeed;
