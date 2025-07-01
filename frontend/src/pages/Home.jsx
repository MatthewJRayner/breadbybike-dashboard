import React, { useState } from 'react';
import Dashboard from '../components/Dashboard';

const HomePage = () => {
    const [location, setLocation] = useState('both');

    const handleRefresh = () => {
        // Optional: Add refresh logic if needed beyond state change
    };

    return (
      <div className='flex-col'>
        <div className="bg-white shadow-md flex p-4 rounded-2xl text-md">
            <h1 className="text-black_text mr-12">BBB Dashboard <span className="text-gray-300"> | Home</span></h1>
            <h1 className="text-black_text mr-3">Location: </h1>
            <div className='bg-bbb-blue-500 rounded-2xl pr-3 pl-3 text-bbb-blue-100'>Both</div>
        </div>
        <div>
            <h1>Home Page</h1>
            <label htmlFor="location">Select Location:</label>
            <select id="location" value={location} onChange={(e) => setLocation(e.target.value)}>
                <option value="both">Both</option>
                <option value="bakery">Bakery</option>
                <option value="cafe">Cafe</option>
            </select>
            <button onClick={handleRefresh}>Refresh Stats</button>
            <Dashboard location={location} itemName={null} />
        </div>
      </div>
    );
};

export default HomePage;