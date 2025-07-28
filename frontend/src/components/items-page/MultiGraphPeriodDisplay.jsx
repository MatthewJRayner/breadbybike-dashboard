import React, { useState, useEffect } from 'react';
import BarChart from '../Graphs/BarChart';
import LineChart from '../Graphs/LineChart';
import Selector from '../Selector';

const MultiGraphPeriodDisplay = ({ stats }) => {
    const [type, setType] = useState('Weekday Average');
    const [period, setPeriod] = useState('Last Month'); 
    const periodKey = period.toLowerCase().replace(/\s+/g, '_');
    const getBarData = (type, period) => {
        if (type === 'Weekday Average') {
            return stats?.[periodKey]?.weekday_average?.graph || [];
        }
        if (type === 'Time of Day Average') {
            return stats?.[periodKey]?.time_of_day_average?.graph || [];
        }
        return [];
    };
    const getBarLabel = (type, period) => {
        if (type === 'Weekday Average') {
            return stats?.[periodKey]?.weekday_average?.labels || [];
        }
        if (type === 'Time of Day Average') {
            return stats?.[periodKey]?.time_of_day_average?.labels || [];
        }
        return [];
    };
    const getLineData = (period) => stats?.[periodKey]?.daily?.graph || [];
    const getLineLabels = (period) => stats?.[periodKey]?.daily?.labels || [];
    const data = type === 'Daily' ? getLineData(period) : getBarData(type, period)
    const labels = type === 'Daily' ? getLineLabels(period) : getBarLabel(type, period)
    const lowestValue = data.length > 0 ? Math.min(...data) : 0
    const highestValue = data.length > 0 ? Math.max(...data) : 0
    const height = 517
    
    // Dynamically change bar thickness
    const numBars = labels.length
    const [chartThickness, setChartThickness] = useState(40);
    useEffect(() => {
        const handleResize = () => {
            const screenWidth = window.innerWidth;

            let baseThickness;
            if (screenWidth < 640) {
                baseThickness = 15;
            } else if (screenWidth < 768) {
                baseThickness = 25;
            } else if (screenWidth < 1024) {
                baseThickness = 35;
            } else {
                baseThickness = 40;
            }

            const maxBars = 16;
            const minThickness = 10;
            const calculated = Math.max(minThickness, Math.min(baseThickness, baseThickness * (maxBars / Math.max(numBars, 1))));

            setChartThickness(calculated);
        };

        handleResize();
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, [numBars])
    const showYLabel= labels.length === 7 ? true : false


    return (
        <div className='bg-white rounded-md shadow-md flex-col'>
            <div className='flex justify-between p-4'>
                <div>
                    <Selector 
                        label='Graph: '
                        value={type}
                        options={['Weekday Average', 'Time of Day Average', 'Daily']}
                        onChange={setType}
                    />
                </div>
                <div>
                    <Selector 
                        label='Period: '
                        value={period}
                        options={['Last Week', 'Last Month', 'Last 3 Months']}
                        onChange={setPeriod}
                    />
                </div>
            </div>
            <div className='p-2'>
                {type === 'Daily'
                    ?
                        <LineChart 
                            data={data}
                            xLabels={labels}
                            yMin={lowestValue - 5}
                            yMax={highestValue + 5}
                            chartHeight={height}
                            chartStep={Math.round((Math.round(highestValue / 20) * 20) / 3)}
                            showYLabel={showYLabel}
                            showXLabel={false}
                            isPercentage={false}
                        />
                    :
                        <BarChart 
                            data={data}
                            xLabels={labels}
                            chartStepSize={Math.round((Math.round(highestValue / 20) * 20) / 3)}
                            chartThickness={chartThickness}
                            showYLabels={false}
                            chartHeight={height}
                        />
                }
            </div>
        </div>
    );
};

export default MultiGraphPeriodDisplay;