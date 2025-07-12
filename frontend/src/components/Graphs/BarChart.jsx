import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const BarChart = ({ xLabels, yLabel = '', data, currency = false, chartHeight, chartThickness, chartStepSize, showLabels = true, showYLabels = true}) => {
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: { top: 0, bottom: 0, left: 0, right: 0 }
        },
        scales: {
            x: {
                ticks: {
                    color: '#666',
                    font: {
                        size: 12,
                    },
                    display: showLabels ? true : false,
                    padding: 0,
                },
                grid: {
                    display: false,
                    drawTicks: showLabels ? true : false,
                    drawBorder: false,
                },
            },
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: chartStepSize,
                    callback: function(value) {
                        return value > 10000 ? `${value / 1000}` : `${value}`;
                    },
                    color: '#666',
                    font: {
                        size: 12,
                    },
                    display: showLabels && showYLabels ? true : false,
                    padding: 0,
                },
                grid: {
                    display: showLabels ? true : false,
                    drawBorder: false,
                    drawTicks: showLabels ? true : false,
                    color: '#bbb',
                    lineWidth: 0.5,
                },
                title: {
                    display: !!yLabel,
                    text: yLabel,
                    color: '#999',
                    font: {
                        size: 14,
                    },
                },
                border: {
                    display: false,
                },
            },
        },
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                displayColors: false,
                callbacks: {
                    label: function(context) {
                        const val = context.parsed.y;
                        return currency ? `£${val.toLocaleString()}` : val.toLocaleString();
                    },
                },
            },
        },
    };

    const chartData = {
        labels: xLabels || [],
        datasets: [
            {
                label: yLabel,
                data,
                backgroundColor: '#143741',
                borderRadius: 4,
                barThickness: chartThickness,
            },
        ],
    };

    return <Bar options={options} data={chartData} height={chartHeight} />
};

export default BarChart