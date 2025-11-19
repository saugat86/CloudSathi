import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

interface TrendChartProps {
    awsData: { date: string; amount: number }[];
    azureData: { date: string; amount: number }[];
}

const TrendChart: React.FC<TrendChartProps> = ({ awsData, azureData }) => {
    // Ensure data is sorted by date
    const sortedAws = [...awsData].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    const sortedAzure = [...azureData].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

    // Get all unique dates
    const allDates = Array.from(new Set([...sortedAws.map(d => d.date), ...sortedAzure.map(d => d.date)])).sort();

    const data = {
        labels: allDates.map(date => {
            const d = new Date(date);
            return `${d.getMonth() + 1}/${d.getDate()}`;
        }),
        datasets: [
            {
                label: 'AWS Spend',
                data: allDates.map(date => sortedAws.find(d => d.date === date)?.amount || 0),
                borderColor: 'rgb(59, 130, 246)', // Blue-500
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true,
                tension: 0.4,
            },
            {
                label: 'Azure Spend',
                data: allDates.map(date => sortedAzure.find(d => d.date === date)?.amount || 0),
                borderColor: 'rgb(14, 165, 233)', // Sky-500
                backgroundColor: 'rgba(14, 165, 233, 0.1)',
                fill: true,
                tension: 0.4,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top' as const,
            },
            tooltip: {
                mode: 'index' as const,
                intersect: false,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)',
                },
            },
            x: {
                grid: {
                    display: false,
                },
            },
        },
        interaction: {
            mode: 'nearest' as const,
            axis: 'x' as const,
            intersect: false,
        },
    };

    return <Line data={data} options={options} />;
};

export default TrendChart;
