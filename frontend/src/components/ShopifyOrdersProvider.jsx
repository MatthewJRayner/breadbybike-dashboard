import React, { useEffect, useState } from 'react';

const ShopifyOrdersProvider = ({ onOrdersLoaded }) => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect (() => {
        const fetchOrders = async () => {
            setLoading(true);
            const url = 'https://breadbybike-dashboard-backend.onrender.com/api/shopify-orders/';
            console.log(`Fetching stats from ${url}`)

            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error(`HTTP Error! Status: ${response.status}`);
                const data = await response.json();
                setOrders(data);
                if (onOrdersLoaded) onOrdersLoaded(data);
            } catch (err) {
                setError(err.message);
                console.error('Fetch error: ', err);
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, []);

    if (loading) return null;
    if (error) return null;

    return null;
};

export default ShopifyOrdersProvider