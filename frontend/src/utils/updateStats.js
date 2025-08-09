const STATS_UPDATE_KEY = 'lastStatsUpdateTime';
const COOLDOWN_TIME = 2 * 60 * 1000; // 2 minutes in ms

export const updateCooldownCheck = () => {
    const storedData = localStorage.getItem(STATS_UPDATE_KEY);
    const parsedData = storedData ? JSON.parse(storedData) : { date: null, time: null };

    const currentDate = new Date().toISOString().split('T')[0];
    const currentTime = Date.now();

    if (!parsedData.date || parsedData.date !== currentDate) {
        localStorage.setItem(
            STATS_UPDATE_KEY,
            JSON.stringify({ date: currentDate, time: currentTime })
        );
        return true;
    }

    const lastUpdateTime = parseInt(parsedData.time);
    if (currentTime - lastUpdateTime > COOLDOWN_TIME) {
        localStorage.setItem(
            STATS_UPDATE_KEY,
            JSON.stringify({ date: currentDate, time: currentTime.toString() })
        );
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