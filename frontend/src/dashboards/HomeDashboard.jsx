import React, { useState } from 'react';
import DashboardDataProvider from '../components/DashboardDataProvider';
import Selector from '../components/Selector';

const HomeDashboard = () => {
    const [location, setLocation] = useState('Both');
    const locations = [location];
    const [stats, setStats] = useState({});

    // Sets the stats dictionary being displaying to change with the location selector
    const handleStatsLoaded = (data) => {
        console.log('Home stats:', data[location]);
        setStats(data)
    };

    return (
        <div className='flex-col'>
            <div className="bg-white shadow-md flex p-4 rounded-2xl text-md items-center">
                <h1 className="text-black_text mr-12">BBB Dashboard <span className="text-gray-300"> | Home</span></h1>
                <Selector 
                    label="Location: "
                    value={location}
                    options={['Both', 'Cafe', 'Bakery']}
                    onChange={setLocation}
                />
            </div>
            <DashboardDataProvider locations={locations} onStatsLoaded={handleStatsLoaded} />
            
            <pre>{JSON.stringify(stats[location], null, 2)}</pre> {/* Placeholder */}
        </div>
    );
};

export default HomeDashboard