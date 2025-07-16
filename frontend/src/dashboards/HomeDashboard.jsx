import React, { useState } from 'react';
import DashboardDataProvider from '../components/DashboardDataProvider';
import Selector from '../components/Selector';
import DailyStatsSummary from '../components/home-page/DailyStatsSummary';
import MonthlyTiles from '../components/home-page/MonthlyTiles';
import BestSellers from '../components/home-page/BestSellers';
import YearSalesDisplay from '../components/home-page/YearSalesDisplay';
import AverageGrowthDisplay from '../components/home-page/AverageGrowthDisplay';
import MonthSalesDisplay from '../components/home-page/MonthSalesDisplay';

const HomeDashboard = () => {
    const [location, setLocation] = useState('Both');
    const locations = [location];
    const [stats, setStats] = useState({});
    var current_month = new Date().toLocaleString("en-us", { month: 'long' });
    var current_year = new Date().toLocaleDateString("en-us", { year: 'numeric' })
    var currency_sym = '£';

    // Sets the stats dictionary being displaying to change with the location selector
    const handleStatsLoaded = (data) => {
        console.log('Home stats:', data[location]);
        setStats(data)
    };

    // Stats dictionaries to be passed through components
    const DailyStatsSummaryStats = [
        { label: 'ITEMS', value: stats[location]?.daily_home_stats?.orders, viewbox: '0 0 576 512', icon_path: 'M0 24C0 10.7 10.7 0 24 0h45.5c22 0 41.5 12.8 50.6 32h411c26.3 0 45.5 25 38.6 50.4l-41 152.3c-8.5 31.4-37 53.3-69.5 53.3H170.7l5.4 28.5c2.2 11.3 12.1 19.5 23.6 19.5H488c13.3 0 24 10.7 24 24s-10.7 24-24 24H199.7c-34.6 0-64.3-24.6-70.7-58.5l-51.6-271c-.7-3.8-4-6.5-7.9-6.5H24C10.7 48 0 37.3 0 24zm128 440a48 48 0 1 1 96 0 48 48 0 1 1-96 0zm336-48a48 48 0 1 1 0 96 48 48 0 1 1 0-96z',},
        { label: 'TOTAL SALES', value: stats[location]?.daily_home_stats?.total_sales, currency: currency_sym, viewbox: '0 0 576 512', icon_path: 'M64 64C28.7 64 0 92.7 0 128v256c0 35.3 28.7 64 64 64h448c35.3 0 64-28.7 64-64V128c0-35.3-28.7-64-64-64H64zm64 320H64v-64c35.3 0 64 28.7 64 64zM64 192v-64h64c0 35.3-28.7 64-64 64zm384 192c0-35.3 28.7-64 64-64v64h-64zm64-192c-35.3 0-64-28.7-64-64h64v64zm-224-32a96 96 0 1 1 0 192 96 96 0 1 1 0-192z'},
        { label: 'DISCOUNTS', value: stats[location]?.daily_home_stats?.discounts, currency: currency_sym, viewbox: '0 0 384 512', icon_path: 'M374.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-320 320c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l320-320zM128 128a64 64 0 1 0-128 0 64 64 0 1 0 128 0zm256 256a64 64 0 1 0-128 0 64 64 0 1 0 128 0z'},
        { label: 'AVERAGE SALE', value: stats[location]?.daily_home_stats?.average_sale, currency: currency_sym, viewbox: '0 0 512 512', icon_path: 'M257.5 27.6c-.8-5.4-4.9-9.8-10.3-10.6-22.1-3.1-44.6.9-64.4 11.4l-74 39.5c-19.7 10.5-35.6 27-45.4 47.1l-36.7 75.6c-9.8 20.1-13 42.9-9.1 64.9l14.5 82.8c3.9 22.1 14.6 42.3 30.7 57.9l60.3 58.4c16.1 15.6 36.6 25.6 58.7 28.7l83 11.7c22.1 3.1 44.6-.9 64.4-11.4l74-39.5c19.7-10.5 35.6-27 45.4-47.2l36.7-75.5c9.8-20.1 13-42.9 9.1-64.9-.9-5.3-5.3-9.3-10.6-10.1-51.5-8.2-92.8-47.1-104.5-97.4-1.8-7.6-8-13.4-15.7-14.6-54.6-8.7-97.7-52-106.2-106.8zM208 144a32 32 0 1 1 0 64 32 32 0 1 1 0-64zm-64 192a32 32 0 1 1 64 0 32 32 0 1 1-64 0zm224-64a32 32 0 1 1 0 64 32 32 0 1 1 0-64z'},
        { label: 'NET SALES', value: stats[location]?.daily_home_stats?.net_sale, currency: currency_sym, viewbox: '0 0 448 512', icon_path: 'M438.6 150.6c12.5-12.5 12.5-32.8 0-45.3l-96-96c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L338.7 96H32c-17.7 0-32 14.3-32 32s14.3 32 32 32h306.7l-41.4 41.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l96-96zm-333.3 352c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 416H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H109.3l41.4-41.4c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-96 96c-12.5 12.5-12.5 32.8 0 45.3l96 96z'},
        { label: 'SERVICE CHARGE', value: stats[location]?.daily_home_stats?.service_charge, currency: currency_sym, viewbox: '0 0 512 512', icon_path: 'M216 64c-13.3 0-24 10.7-24 24s10.7 24 24 24h16v33.3C119.6 157.2 32 252.4 32 368h448c0-115.6-87.6-210.8-200-222.7V112h16c13.3 0 24-10.7 24-24s-10.7-24-24-24h-80zM24 400c-13.3 0-24 10.7-24 24s10.7 24 24 24h464c13.3 0 24-10.7 24-24s-10.7-24-24-24H24z'},
    ];

    const MonthlyTilesStats = [
        { label: `Total Sales (${current_month})`, value: stats[location]?.monthly_stats_tiles?.total_sales_month, currency: currency_sym, viewbox: '0 0 576 512', icon_path: 'M64 32C28.7 32 0 60.7 0 96v32h576V96c0-35.3-28.7-64-64-64H64zm512 192H0v192c0 35.3 28.7 64 64 64h448c35.3 0 64-28.7 64-64V224zM112 352h64c8.8 0 16 7.2 16 16s-7.2 16-16 16h-64c-8.8 0-16-7.2-16-16s7.2-16 16-16zm112 16c0-8.8 7.2-16 16-16h128c8.8 0 16 7.2 16 16s-7.2 16-16 16H240c-8.8 0-16-7.2-16-16z'},
        { label: `Net Sales (${current_month})`, value: stats[location]?.monthly_stats_tiles?.net_sales_month, currency: currency_sym, viewbox: '0 0 448 512', icon_path: 'M160 112c0-35.3 28.7-64 64-64s64 28.7 64 64v48H160v-48zm-48 48H48c-26.5 0-48 21.5-48 48v208c0 53 43 96 96 96h256c53 0 96-43 96-96V208c0-26.5-21.5-48-48-48h-64v-48C336 50.1 285.9 0 224 0S112 50.1 112 112v48zm24 48a24 24 0 1 1 0 48 24 24 0 1 1 0-48zm152 24a24 24 0 1 1 48 0 24 24 0 1 1-48 0z'},
        { label: `Average Sale (${current_month})`, value: stats[location]?.monthly_stats_tiles?.average_sale_month, currency: currency_sym, viewbox: '0 0 512 512', icon_path: 'M247.2 17c-22.1-3.1-44.6.9-64.4 11.4l-74 39.5c-19.7 10.5-35.6 27-45.4 47.1l-36.7 75.6c-9.8 20.1-13 42.9-9.1 64.9l14.5 82.8c3.9 22.1 14.6 42.3 30.7 57.9l60.3 58.4c16.1 15.6 36.6 25.6 58.7 28.7l83 11.7c22.1 3.1 44.6-.9 64.4-11.4l74-39.5c19.7-10.5 35.6-27 45.4-47.2l36.7-75.5c9.8-20.1 13-42.9 9.1-64.9l-14.6-82.8c-3.9-22.1-14.6-42.3-30.7-57.9l-60.2-58.3c-16.1-15.6-36.6-25.6-58.7-28.7l-83-11.8zM208 144a32 32 0 1 1 0 64 32 32 0 1 1 0-64zm-64 192a32 32 0 1 1 64 0 32 32 0 1 1-64 0zm224-64a32 32 0 1 1 0 64 32 32 0 1 1 0-64z'},
        { label: `Items Sold (${current_month})`, value: stats[location]?.monthly_stats_tiles?.items_sold, viewbox: '0 0 448 512', icon_path: 'M0 80v149.5c0 17 6.7 33.3 18.7 45.3l176 176c25 25 65.5 25 90.5 0l133.5-133.5c25-25 25-65.5 0-90.5l-176-176c-12-12-28.3-18.7-45.3-18.7L48 32C21.5 32 0 53.5 0 80zm112 32a32 32 0 1 1 0 64 32 32 0 1 1 0-64z'},
    ];

    return (
        <div className='flex-col'>
            <DashboardDataProvider locations={locations} onStatsLoaded={handleStatsLoaded} />
            <div className="bg-white shadow-md flex p-4 rounded-2xl text-md items-center">
                <h1 className="text-black_text mr-12">BBB Dashboard <span className="text-gray-300"> | Home</span></h1>
                <Selector 
                    label="Location: "
                    value={location}
                    options={['Both', 'Cafe', 'Bakery']}
                    onChange={setLocation}
                />
            </div>
            {/* Load Stats from model */}
            <div className='w-full flex'>
                {/* Left Side */}
                <div className='w-1/2 flex-col mr-2'>
                    <div className='mt-4 w-full'>
                        <DailyStatsSummary stats={DailyStatsSummaryStats} />
                    </div>
                    <div className='grid grid-cols-2 mt-4 w-full justify-between'>
                        <div className='mr-2'>
                            <AverageGrowthDisplay stats={stats[location]?.average_growth_graph} label={'Average Growth'} desc={'Growth to same day previous week'} bottomLabel={'Previous 2 Weeks'}/>
                        </div>
                        <div className='ml-2'>
                            <MonthSalesDisplay stats={stats[location]?.monthly_sales_graph} label={`Total Sales`} desc={'Total Sales over last 30 days'} />
                        </div>
                    </div>
                    <div className='mt-4 w-full'>
                        <BestSellers stats={stats[location]?.best_sellers}/>
                    </div>
                </div>
                {/* Right Side */}
                <div className='w-1/2 flex-col ml-2'>
                    <div className='mt-4 w-full'>
                        <YearSalesDisplay stats={stats[location]?.year_sales_graph} title={`${current_year} Sales (${location})`} label1={'Total Sales'} label2={'Monthly Average'} height={300} />
                    </div>
                    <div className='mt-4 w-full'>
                        <MonthlyTiles stats={MonthlyTilesStats} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomeDashboard