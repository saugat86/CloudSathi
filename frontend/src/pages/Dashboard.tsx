import React, { useState, useEffect } from 'react';
import {
    TrendingUp,
    DollarSign,
    ArrowUpRight,
    ArrowDownRight,
    Target,
    AlertTriangle
} from 'lucide-react';
import { costService } from '../services/costService';
import { AWSCostResponse, AzureCostResponse } from '../types/cost';
import { formatCurrency, getDateDaysAgo, getTodayDate } from '../utils/formatters';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';
import TrendChart from '../components/TrendChart';
import { sampleBudget, sampleFindings } from '../services/mockData';

const Dashboard: React.FC = () => {
    const [awsCosts, setAwsCosts] = useState<(AWSCostResponse & { daily_costs?: any[] }) | null>(null);
    const [azureCosts, setAzureCosts] = useState<(AzureCostResponse & { daily_costs?: any[] }) | null>(null);
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
    const potentialSavings = sampleFindings.reduce((acc, curr) => acc + curr.estimated_monthly_savings, 0);
    const budgetUsagePercent = (sampleBudget.current_spend / sampleBudget.total_budget) * 100;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">FinOps Dashboard</h1>
                    <p className="mt-1 text-sm text-gray-500">
                        Overview of cloud spend, budget health, and optimization opportunities.
                    </p>
                </div>
                <div className="flex items-center space-x-3">
                    <span className="text-sm text-gray-500 bg-white px-3 py-1 rounded-md border border-gray-200 shadow-sm">
                        {startDate} - {endDate}
                    </span>
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
                        Export Report
                    </button>
                </div>
            </div>

            {error && <ErrorAlert message={error} onDismiss={() => setError(null)} />}

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Total Spend */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-medium text-gray-500">Total Spend (MTD)</h3>
                        <div className="p-2 bg-blue-50 rounded-lg">
                            <DollarSign className="h-5 w-5 text-blue-600" />
                        </div>
                    </div>
                    <div className="flex items-baseline">
                        <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalCost)}</p>
                        <span className="ml-2 text-sm font-medium text-green-600 flex items-center">
                            <ArrowDownRight className="h-4 w-4 mr-1" />
                            2.5%
                        </span>
                    </div>
                    <p className="mt-1 text-xs text-gray-500">vs last month</p>
                </div>

                {/* Forecast */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-medium text-gray-500">Forecasted Spend</h3>
                        <div className="p-2 bg-purple-50 rounded-lg">
                            <TrendingUp className="h-5 w-5 text-purple-600" />
                        </div>
                    </div>
                    <div className="flex items-baseline">
                        <p className="text-2xl font-bold text-gray-900">{formatCurrency(sampleBudget.forecasted_spend)}</p>
                        <span className="ml-2 text-sm font-medium text-red-600 flex items-center">
                            <ArrowUpRight className="h-4 w-4 mr-1" />
                            5.2%
                        </span>
                    </div>
                    <p className="mt-1 text-xs text-gray-500">Projected month end</p>
                </div>

                {/* Budget Health */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-medium text-gray-500">Budget Health</h3>
                        <div className="p-2 bg-green-50 rounded-lg">
                            <Target className="h-5 w-5 text-green-600" />
                        </div>
                    </div>
                    <div className="flex items-baseline mb-2">
                        <p className="text-2xl font-bold text-gray-900">{budgetUsagePercent.toFixed(1)}%</p>
                        <span className="ml-2 text-sm text-gray-500">used</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                            className={`h-2 rounded-full ${budgetUsagePercent > 90 ? 'bg-red-500' : 'bg-green-500'}`}
                            style={{ width: `${Math.min(budgetUsagePercent, 100)}%` }}
                        ></div>
                    </div>
                    <p className="mt-2 text-xs text-gray-500">
                        {formatCurrency(sampleBudget.current_spend)} of {formatCurrency(sampleBudget.total_budget)}
                    </p>
                </div>

                {/* Potential Savings */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-medium text-gray-500">Potential Savings</h3>
                        <div className="p-2 bg-yellow-50 rounded-lg">
                            <AlertTriangle className="h-5 w-5 text-yellow-600" />
                        </div>
                    </div>
                    <div className="flex items-baseline">
                        <p className="text-2xl font-bold text-gray-900">{formatCurrency(potentialSavings)}</p>
                        <span className="ml-2 text-sm text-gray-500">/ month</span>
                    </div>
                    <p className="mt-1 text-xs text-gray-500">{sampleFindings.length} opportunities identified</p>
                </div>
            </div>

            {/* Trend Chart */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">Daily Spend Trend (30 Days)</h3>
                <div className="h-80">
                    <TrendChart
                        awsData={awsCosts?.daily_costs || []}
                        azureData={azureCosts?.daily_costs || []}
                    />
                </div>
            </div>

            {/* Cost Breakdown Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* AWS Breakdown */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Top AWS Services</h3>
                    <div className="space-y-4">
                        {awsCosts?.costs_by_service.slice(0, 5).map((service, index) => (
                            <div key={index} className="flex items-center justify-between">
                                <div className="flex items-center">
                                    <div className="w-2 h-2 rounded-full bg-blue-500 mr-3"></div>
                                    <span className="text-sm text-gray-700 truncate max-w-[200px]">{service.service_name}</span>
                                </div>
                                <span className="text-sm font-medium text-gray-900">{formatCurrency(service.amount)}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Azure Breakdown */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Azure Resource Groups</h3>
                    <div className="space-y-4">
                        {azureCosts?.costs_by_resource_group.slice(0, 5).map((rg, index) => (
                            <div key={index} className="flex items-center justify-between">
                                <div className="flex items-center">
                                    <div className="w-2 h-2 rounded-full bg-sky-500 mr-3"></div>
                                    <span className="text-sm text-gray-700 truncate max-w-[200px]">{rg.resource_group}</span>
                                </div>
                                <span className="text-sm font-medium text-gray-900">{formatCurrency(rg.amount)}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
