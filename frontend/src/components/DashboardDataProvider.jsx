import React, { useState, useEffect } from 'react';

const DashboardDataProvider = ({ locations, onStatsLoaded }) => {
    const [stats, setStats] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchStats = async () => {
            setLoading(true);
            const url = `${import.meta.env.VITE_API_URL}/api/order-stats/?locations=${locations.join(',')}`;
            console.log(`fetching from: ${url}`);

            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const data = await response.json();
                setStats(data);
                if (onStatsLoaded) onStatsLoaded(data);
            } catch (err) {
                setError(err.message);
                console.error('Fetch error: ', err);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, [locations.join(',')]);

    if (loading) return null
    if (error) return null

    return null;
};

export default DashboardDataProvider;