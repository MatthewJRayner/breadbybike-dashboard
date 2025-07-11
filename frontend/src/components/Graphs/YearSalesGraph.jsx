import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Tooltip, Legend } from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Tooltip, Legend);

const YearSalesGraph = ({ data }) => {
    var current_year = new Date().toLocaleString("en-us", { year: 'long' })
    const chartData = {
        labels: data.labels,
        datasets: [
            {
                label: `Monthly Sales ${current_year}`,
                data: Object.values(data.graph),
                backgroundColor: '#143741'
            }
        ]
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: { callbacks: { label: ctx => `£${ctx.raw.toLocaleString()}` } }
        },
        scales: {
            y: { beginAtZero: true}
        }
    };

    return (
        <Bar data={chartData} options={options} />
    );
};

export default YearSalesGraph