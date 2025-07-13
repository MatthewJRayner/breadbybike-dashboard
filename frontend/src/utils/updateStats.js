const STATS_UPDATE_KEY = 'lastStatsUpdateTime';
const COOLDOWN_TIME = 5000; // 5 seconds in ms
const STATS_READY_TIMEOUT = 7000;
const STATS_READY_CHECK_INTERVAL = 1000;

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
        const response = await fetch('http://localhost:8000/api/update-daily-stats/', {
            method: 'POST',
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Failed to update stats:', errorData.error || response.statusText);
            throw new Error(errorData.error || 'Update failed');
        } 
        
        console.log('Stats update triggered. Waiting for updated values...');

        const start = Date.now();
        while (Date.now() - start < STATS_READY_TIMEOUT) {
            const check = await fetch('http://localhost:8000/api/order-stats/?locations=Both');
            if (!check.ok) throw new Error('Failed to fetch stats after update.');

            const data = await check.json();
            const total = data?.daily_home_stats?.total_sales;

            if (total && total > 0) {
                console.log('Stats confirmed updated.');
                return;
            }

            await new Promise((resolve) => setTimeout(resolve, STATS_READY_CHECK_INTERVAL));
        }

        console.warn('Stats did not update in time. Proceeding anyway...');
    } catch (error) {
        console.error('Error updating stats:', error);
        throw error;
    }
};