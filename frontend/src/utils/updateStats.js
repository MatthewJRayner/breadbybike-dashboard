const STATS_UPDATE_KEY = 'lastStatsUpdateTime';
const COOLDOWN_TIME = 2 * 60 * 1000; // 2 minutes in ms

export const updateCooldownCheck = () => {
    const lastUpdate = localStorage.getItem(STATS_UPDATE_KEY);
    const currentTime = Date.now();

    if (!lastUpdate || currentTime - parseInt(lastUpdate) > COOLDOWN_TIME) {
        localStorage.setItem(STATS_UPDATE_KEY, currentTime.toString());
        return true;
    }
    return false;
};

export const triggerStatsUpdate = async () => {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/update-daily-stats/`, {
            method: 'POST',
        });
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Failed to update stats:', errorData.error || response.statusText);
            throw new Error(errorData.error || 'Update failed');
        } else {
            console.log('Daily stats updated successfully.');
        }
    } catch (error) {
        console.error('Error updating stats:', error);
        throw error;
    }
};