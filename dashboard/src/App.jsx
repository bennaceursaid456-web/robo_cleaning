import React, { useState, useEffect } from 'react';
import DashboardLayout from './components/layout/DashboardLayout';
import StatCard from './components/dashboard/StatCard';
import VideoFeed from './components/dashboard/VideoFeed';
import AIAdvisor from './components/dashboard/AIAdvisor';
import { api } from './services/api';

function App() {
  const [stats, setStats] = useState({
    total_objects: 0,
    recyclable: 0,
    toxic: 0,
    human: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      const data = await api.getStats();
      if (data) {
        setStats(prev => ({
          ...data,
          // Ensure we have an array ensuring safety if backend is old
          active: data.active || []
        }));
      }
    };

    fetchStats(); // Initial fetch
    const interval = setInterval(fetchStats, 500); // Poll faster (0.5s) for better glow reactivity

    return () => clearInterval(interval);
  }, []);

  return (
    <DashboardLayout>

      {/* Left Sidebar: Status Panel */}
      <aside className="sidebar-panel">
        <div className="panel-section-title">System Status</div>

        <StatCard
          icon="📦"
          label="Total Detected"
          value={stats.total_objects}
        />
        <StatCard
          icon="♻️"
          label="Recyclable"
          value={stats.recyclable}
          color="var(--color-accent-green)"
          isActive={stats.active?.includes('recyclable')}
        />
        <StatCard
          icon="☣️"
          label="Toxic / Hazardous"
          value={stats.toxic}
          color="var(--color-accent-red)"
          isActive={stats.active?.includes('toxic')}
        />

        <div className={`stat-card alert-card ${stats.human > 0 ? '' : 'inactive'}`} style={{ marginTop: 'auto', opacity: stats.human > 0 ? 1 : 0.5 }}>
          <div className="stat-icon" style={{ color: 'var(--color-accent-orange)' }}>
            👤
          </div>
          <div className="stat-content">
            <span className="stat-label">Human Presence</span>
            <span className="stat-value" style={{ fontSize: '1rem', color: 'var(--color-accent-orange)' }}>
              {stats.human > 0 ? 'DETECTED — PAUSED' : 'NONE DETECTED'}
            </span>
          </div>
        </div>
      </aside>

      {/* Center: Video Feed */}
      <VideoFeed
        activeCategories={stats.active || []}
      />

      {/* Right: AI Advisor */}
      <AIAdvisor />

    </DashboardLayout>
  );
}

export default App;
