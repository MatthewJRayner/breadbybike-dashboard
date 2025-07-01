import React, { useState, useEffect } from 'react';

const Dashboard = ({ location, itemName }) => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchStats = async () => {
            setLoading(true);
            const locations = itemName ? `${location},${location}_items_${itemName}` : location;
            const url = `/api/order-stats/?locations=${locations}`;

            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error('Failed to fetch stats');
                const data = await response.json();
                setStats(itemName ? data[`${location}_items_${itemName}`] : data[location]);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, [location, itemName]);  // Re-fetch when location or itemName changes

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h2>{itemName ? `Items Stats for ${itemName}` : `Home Stats for ${location}`}</h2>
            <pre>{JSON.stringify(stats, null, 2)}</pre>
            {/* Replace with your chart or UI components */}
        </div>
    );
};

export default Dashboard;