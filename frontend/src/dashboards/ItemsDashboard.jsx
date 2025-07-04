import React, { useState, useEffect } from 'react';
import DashboardDataProvider from '../components/DashboardDataProvider';
import Selector from '../components/Selector';

const ItemsDashboard = () => {
    const [location, setLocation] = useState('Both');
    const [itemName, setName] = useState('Cinnamon');
    const [items, setItems] = useState([]);
    const [locations, setLocations] = useState([location, `${location}_items_${itemName}`]);
    const [stats, setStats] = useState({});
    const [needsCalculation, setNeedsCalculation] = useState(false);
    const [loading, setLoading] = useState(false);

    // Fetch Square catalog items
    useEffect(() => {
        const fetchCatalogItems = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/square-catalog-items/');
                if (!response.ok) throw new Error('Failed to fetch catalog items');
                const data = await response.json();
                if (data.items) {
                    setItems(data.items);
                }
            } catch (error) {
                console.error('Error fetching catalog items:', error);
            }
        };
        fetchCatalogItems();
    }, []);

    useEffect(() => {
        setLocations([location, `${location}_items_${itemName}`]);
    }, [location, itemName]);

    // Checks whether there needs to be a new calculation to display item specific stats
    const handleItemChange = (newItemName) => {
        setName(newItemName);
        const itemLocation = `${location}_items_${newItemName}`;
        setNeedsCalculation(!stats[itemLocation])
    };

    const handleStatsLoaded = (data) => {
        console.log('Items Stats:', data);
        setStats(prevStats => ({ ...prevStats, ...data }));
    };

    // POST the location and item name to be calculated and added to OrderStats model in the backend
    const triggerCalculation = async (loc, item) => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/trigger-calculation/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location: loc, item_name: item }),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to trigger calculation');
            }

            console.log('Calculation triggered successfully');
            const updatedStats = await fetchStats(locations);
            setStats(updatedStats);
            setNeedsCalculation(false);
        } catch (error) {
            console.error('Error triggering calculation:', error);
            alert(`Calculation failed: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const fetchStats = async (locs) => {
        const response = await fetch(`http://localhost:8000/api/order-stats/?locations=${locs.join(',')}`);
        if (!response.ok) {
            console.error('Failed to fetch stats:', await response.text());
        }
        const data = await response.json();
        console.log('Fetched stats:', data);
        return data;
    }

    return (
        <div className='flex-col'>
            <div className="bg-white shadow-md flex p-4 rounded-2xl text-md items-center">
                <h1 className="text-black_text mr-12">BBB Dashboard <span className="text-gray-300"> | Items</span></h1>
                <Selector 
                    label="Location: "
                    value={location}
                    options={['Both', 'Cafe', 'Bakery']}
                    onChange={setLocation}
                />
                <Selector 
                    label="Items: "
                    value={itemName}
                    options={items}
                    onChange={handleItemChange}
                />
                {needsCalculation && (
                    <button
                        className="ml-4 px-4 py-2 bg-bbb-blue-500 text-white rounded-lg hover:bg-bbb-blue-800 disabled:opacity-50"
                        onClick={() => triggerCalculation(location, itemName)}
                        disabled={loading} // Disable during loading
                    >
                        {loading ? 'Calculating...' : 'Calculate New Item Stats'}
                    </button>
                )}
            </div>
            <DashboardDataProvider
                key={`${location}-${itemName}-${needsCalculation}-${loading}`}
                locations={locations}
                onStatsLoaded={handleStatsLoaded}
            />

            <pre>{JSON.stringify(stats[`${location}_items_${itemName}`], null, 2)}</pre> {/* Placeholder */}
        </div>

    );
};

export default ItemsDashboard