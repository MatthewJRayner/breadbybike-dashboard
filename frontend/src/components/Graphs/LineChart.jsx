import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

const LineChart = ({ xLabels, data, yLabel = '', chartHeight = 200, currency = false, chartStep, showYLabel = true, showYGrid = true, showOnlyZeroLine = false, yMin, yMax, showLabels = true, showXLabel = true, isPercentage = true }) => {
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: {
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
            },
        },
        scales: {
            x: {
                ticks: {
                    color: '#666',
                    font: {
                        size: 8,
                    },
                    display: showLabels && showXLabel ? true : false,
                    padding: 0,
                },
                grid: {
                    drawTicks: false,
                    drawBorder: false,
                    display: false,
                },
            },
            y: {
                min: yMin,
                max: yMax,
                ticks: {
                    display: showYLabel ? true : false,
                    stepSize: chartStep,
                    callback: function (value) {
                        if (showOnlyZeroLine && value !== 0) return '';
                        if (currency) return `£${value.toLocaleString()}`;
                        return `${value.toLocaleString()}`;
                    },
                    color: '#666',
                    font: {
                        size: 8,
                    },
                    padding: 0,
                },
                title: {
                    display: !!yLabel,
                    text: yLabel,
                    color: '#999',
                    font: {
                        size: 8,
                    },
                },
                grid: {
                    drawTicks: showYLabel ? true : false,
                    drawBorder: false,
                    color: (ctx) => (ctx.tick.value === 0 ? '#bbb' : showYGrid ? '#bbb' : 'white'),
                    lineWidth: (ctx) => (ctx.tick.value === 0 ? 2 : 0.5),
                },
                border: {
                    display: false
                },
            },
        },
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                callbacks: {
                    label: context => `${isPercentage ? `${context.parsed.y.toFixed(2)}%` : `${context.parsed.y}`}`,
                },
            },
        },
    };

    const chartData = {
        labels: xLabels,
        datasets: [
            {
                label: yLabel,
                data,
                borderColor: '#143741',
                backgroundColor: '#143741',
                tension: 0.3,
                pointRadius: 2,
                pointBackgroundColor: '#143741',
                fill: origin,
            },
        ],
    };

    return <Line options={options} data={chartData} height={chartHeight} />;
};

export default LineChart