import React, { useState, useEffect } from 'react';
import { Cloud, TrendingUp, DollarSign, Calendar } from 'lucide-react';
import { costService } from '../services/costService';
import { AWSCostResponse, AzureCostResponse } from '../types/cost';
import { formatCurrency, getDateDaysAgo, getTodayDate } from '../utils/formatters';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const Dashboard: React.FC = () => {
    const [awsCosts, setAwsCosts] = useState<AWSCostResponse | null>(null);
    const [azureCosts, setAzureCosts] = useState<AzureCostResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const startDate = getDateDaysAgo(30);
    const endDate = getTodayDate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);

                const [awsData, azureData] = await Promise.allSettled([
                    costService.getAWSCosts(startDate, endDate),
                    costService.getAzureCosts(startDate, endDate),
                ]);

                if (awsData.status === 'fulfilled') {
                    setAwsCosts(awsData.value);
                }
                if (azureData.status === 'fulfilled') {
                    setAzureCosts(azureData.value);
                }

                if (awsData.status === 'rejected' && azureData.status === 'rejected') {
                    setError('Failed to fetch cost data. Please check your API connection.');
                }
            } catch (err) {
                setError('An unexpected error occurred');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [startDate, endDate]);

    if (loading) {
        return <LoadingSpinner message="Loading dashboard data..." />;
    }

    const totalCost = (awsCosts?.total_cost || 0) + (azureCosts?.total_cost || 0);

    // Prepare chart data for AWS
    const awsChartData = awsCosts ? {
        labels: awsCosts.costs_by_service.map(s => s.service_name),
        datasets: [{
            data: awsCosts.costs_by_service.map(s => s.amount),
            backgroundColor: [
                '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
                '#EC4899', '#14B8A6', '#F97316', '#6366F1', '#84CC16'
            ],
        }],
    } : null;

    // Prepare chart data for Azure
    const azureChartData = azureCosts ? {
        labels: azureCosts.costs_by_resource_group.map(rg => rg.resource_group),
        datasets: [{
            data: azureCosts.costs_by_resource_group.map(rg => rg.amount),
            backgroundColor: [
                '#0078D4', '#50E6FF', '#00BCF2', '#00B294', '#FFB900',
                '#E81123', '#B4009E', '#5C2D91', '#008272', '#00CC6A'
            ],
        }],
    } : null;

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Cloud Cost Dashboard</h1>
                <p className="mt-2 text-gray-600">
                    Overview of your cloud spending for the last 30 days
                </p>
            </div>

            {error && (
                <div className="mb-6">
                    <ErrorAlert message={error} onDismiss={() => setError(null)} />
                </div>
            )}

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Total Cost</p>
                            <p className="mt-2 text-3xl font-bold text-gray-900">
                                {formatCurrency(totalCost)}
                            </p>
                        </div>
                        <DollarSign className="h-12 w-12 text-blue-600" />
                    </div>
                </div>

                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">AWS Costs</p>
                            <p className="mt-2 text-3xl font-bold text-gray-900">
                                {formatCurrency(awsCosts?.total_cost || 0)}
                            </p>
                        </div>
                        <Cloud className="h-12 w-12 text-orange-600" />
                    </div>
                </div>

                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Azure Costs</p>
                            <p className="mt-2 text-3xl font-bold text-gray-900">
                                {formatCurrency(azureCosts?.total_cost || 0)}
                            </p>
                        </div>
                        <Cloud className="h-12 w-12 text-blue-600" />
                    </div>
                </div>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {awsChartData && (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">
                            AWS Costs by Service
                        </h2>
                        <div className="h-64">
                            <Pie data={awsChartData} options={{ maintainAspectRatio: false }} />
                        </div>
                    </div>
                )}

                {azureChartData && (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">
                            Azure Costs by Resource Group
                        </h2>
                        <div className="h-64">
                            <Pie data={azureChartData} options={{ maintainAspectRatio: false }} />
                        </div>
                    </div>
                )}
            </div>

            {/* Period Info */}
            <div className="mt-6 flex items-center text-sm text-gray-600">
                <Calendar className="h-4 w-4 mr-2" />
                <span>Period: {startDate} to {endDate}</span>
            </div>
        </div>
    );
};

export default Dashboard;
