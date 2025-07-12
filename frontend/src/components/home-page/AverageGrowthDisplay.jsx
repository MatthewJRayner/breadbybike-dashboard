import React from 'react';
import LineChart from '../Graphs/LineChart';

const AverageGrowthDisplay = ({ stats, label, desc, bottomLabel }) => {
    const data = stats?.graph || [];
    const labels = stats?.labels || [];
    const lowestValue = data.length > 0 ? Math.min(...data) : 0;
    const highestValue = data.length > 0 ? Math.max(...data) : 0;
    const getPercentageColour = (key, defaultValue = 0) => {
        const value = stats?.percentages?.[key] ?? defaultValue;
        return value >= 0 ? 'text-green-700' : 'text-red-700';
    };

    const weekColour = getPercentageColour('previous_week');
    const yearColour = getPercentageColour('previous_year');

    return (
        <div className='bg-white rounded-md shadow-md flex-col w-full'>
            <div className='p-4'>
                <div className='flex-col mb-4 text-left'>
                    <div className='flex mb-2 items-center'>
                        <div className='flex-col mr-4'>
                            <div className='text-black_text font-semibold text-md'>{stats?.average_growth}%</div>
                            <div className='text-bbb-blue-600 font-semibold text-xs'>{label}</div>
                        </div>
                        <div className='flex-col text-xs text-center font-medium'>
                            <div className={`${weekColour}`}>{stats?.percentages?.previous_week}%</div>
                            <div className={`${yearColour}`}>{stats?.percentages?.previous_year}%</div>
                        </div>
                    </div>
                    <div className='text-gray-400 text-left text-[10px]'>{desc}</div>
                </div>
                <div className='w-full'>
                    <LineChart 
                        xLabels={labels}
                        data={data}
                        chartStep={highestValue + 10}
                        showYLabel={false}
                        yMin={lowestValue - 5}
                        yMax={highestValue + 5}
                        chartHeight={100}
                    />
                </div>
            </div>
            <div className='flex-col justify-center items-center bg-bbb-blue-500 rounded-b-md text-white p-2 w-full'>
                <div className='flex text-xs font-semibold justify-center mb-1'>
                    <div className='mr-4'>{stats?.previous_3_weeks?.week0}%</div>
                    <div>{stats?.previous_3_weeks?.week1}%</div>
                </div>
                <div className='text-xs'>{bottomLabel}</div>
            </div>
        </div>
    );
};

export default AverageGrowthDisplay