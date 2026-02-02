import React, { useState, useEffect } from 'react';
import '../../styles/dashboard.css';
import { api } from '../../services/api';

const AIAdvisor = () => {
    const [logs, setLogs] = useState([
        { type: 'info', message: 'System initialization complete', time: new Date().toLocaleTimeString() }
    ]);

    useEffect(() => {
        let lastAlertId = null;
        let lastAdvice = null;

        const fetchAlerts = async () => {
            const alert = await api.getAlert();

            // Update if:
            // 1. It's a completely new object (ID changed)
            // 2. It's the same object, but the AI advice has arrived/changed
            if (alert && (alert.id !== lastAlertId || alert.advice !== lastAdvice)) {

                // If it's just an update to the SAME log (same ID), replace the last log
                // Otherwise add a new log
                const isUpdate = (alert.id === lastAlertId);

                lastAlertId = alert.id;
                lastAdvice = alert.advice;

                const newLog = {
                    id: alert.id, // Track ID for future updates
                    type: alert.type === 'toxic' ? 'warning' : 'info',
                    message: `${alert.type.toUpperCase()}: ${alert.label}`,
                    subtext: alert.advice, // New field for AI text
                    time: new Date().toLocaleTimeString()
                };

                setLogs(prevLogs => {
                    if (isUpdate && prevLogs.length > 0 && prevLogs[0].id === alert.id) {
                        // Update the most recent log in place
                        const updated = [...prevLogs];
                        updated[0] = newLog;
                        return updated;
                    }
                    // Insert new
                    return [newLog, ...prevLogs].slice(0, 50);
                });
            }
        };

        const interval = setInterval(fetchAlerts, 2000); // Check for alerts every 2s
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="advisor-panel">
            <div className="advisor-header">
                <span>🤖</span>
                <span>AI ADVISOR</span>
            </div>
            <div className="advisor-content">
                {logs.map((log, index) => (
                    <div key={index} className={`log-item ${log.type}`}>
                        <div className="log-msg">
                            <strong>{log.message}</strong>
                            {log.subtext && (
                                <div style={{
                                    marginTop: '4px',
                                    opacity: 0.9,
                                    fontStyle: 'italic',
                                    fontSize: '0.85rem',
                                    borderLeft: '2px solid rgba(255,255,255,0.2)',
                                    paddingLeft: '8px'
                                }}>
                                    {log.subtext}
                                </div>
                            )}
                        </div>
                        <span className="log-time">{log.time}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AIAdvisor;
