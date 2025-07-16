import React, { useState, useEffect } from 'react';
import DashboardDataProvider from '../components/DashboardDataProvider';
import Selector from '../components/Selector';
import StatsBlock from '../components/StatsBlock';
import DailyAverage from '../components/items-page/DailyAverage';
import RecentTime from '../components/items-page/RecentTime';
import WeekSalesDisplay from '../components/items-page/WeekSalesDisplay';
import MultiGraphPeriodDisplay from '../components/items-page/MultiGraphPeriodDisplay';

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
            <DashboardDataProvider
                key={`${location}-${itemName}-${needsCalculation}-${loading}`}
                locations={locations}
                onStatsLoaded={handleStatsLoaded}
            />
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
                        className="ml-4 p-2 bg-bbb-blue-500 text-white rounded-lg hover:bg-bbb-blue-800 disabled:opacity-50"
                        onClick={() => triggerCalculation(location, itemName)}
                        disabled={loading} // Disable during loading
                    >
                        {loading ? 'Calculating...' : 
                            <div>
                                <svg className='size-4 fill-current' viewBox='0 0 512 512'>
                                    <path d='M416 208c0 45.9-14.9 88.3-40 122.7l126.6 126.7c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0s208 93.1 208 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z'></path>
                                </svg>
                            </div>}
                    </button>
                )}
            </div>
            <div className='w-full flex'>
                {/* Left Side */}
                <div className='w-2/3 flex-col mt-4 mr-2'>
                    <div className='w-full flex'>
                        <div className='w-1/2 mr-2'>
                            <StatsBlock label='DAILY SALES' value={stats[`${location}_items_${itemName}`]?.daily_items_stats?.daily_sales?.sales} percentage={stats[`${location}_items_${itemName}`]?.daily_items_stats?.daily_sales?.percentage} />
                        </div>
                        <div className='w-1/2 ml-2'>
                            <StatsBlock label='WEEKLY SALES' value={stats[`${location}_items_${itemName}`]?.weekly_sales?.sales} percentage={stats[`${location}_items_${itemName}`]?.weekly_sales?.percentage} />
                        </div>
                    </div>
                    <div className='w-full mt-4'>
                        <MultiGraphPeriodDisplay stats={stats[`${location}_items_${itemName}`]?.period_graphs}/>
                    </div>
                </div>
                {/* Right Side */}
                <div className='w-1/3 flex-col mt-4 ml-2'>
                    <div className='w-full'>
                        <StatsBlock label='MONTHLY SALES' value={stats[`${location}_items_${itemName}`]?.monthly_sales?.sales} percentage={stats[`${location}_items_${itemName}`]?.monthly_sales?.percentage} />
                    </div>
                    <div className='w-full mt-4'>
                        <WeekSalesDisplay stats={stats[`${location}_items_${itemName}`]?.total_sales_last_week} label={'Total Sales (Last Week)'}/>
                    </div>
                    <div className='mt-4 w-full'>
                        <DailyAverage label='Daily Average (Last 7 Days)' count={stats[`${location}_items_${itemName}`]?.daily_average?.count} percent1={stats[`${location}_items_${itemName}`]?.daily_average?.percentage?.previous_week} percent2={stats[`${location}_items_${itemName}`]?.daily_average?.percentage?.previous_month} />
                    </div>
                    <div className='mt-4 w-full'>
                        <RecentTime label='Recent Time (Yesterday)' time={stats[`${location}_items_${itemName}`]?.daily_items_stats?.recent_time} />
                    </div>
                </div>
            </div>
        </div>

    );
};

export default ItemsDashboard