const API_BASE_URL = 'http://localhost:8000';

export const api = {
    // Get current statistics
    getStats: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/stats`);
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('Error fetching stats:', error);
            return null;
        }
    },

    // Get the latest alert
    getAlert: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/alert`);
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('Error fetching alert:', error);
            return null;
        }
    },

    // Video stream URL
    videoStreamUrl: `${API_BASE_URL}/video`
};
