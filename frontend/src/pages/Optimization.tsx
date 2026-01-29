import React, { useState } from 'react';
import {
    AlertTriangle,
    Filter,
    ArrowRight,
    Server,
    Database,
    HardDrive
} from 'lucide-react';
import { sampleFindings, OptimizationFinding } from '../services/mockData';
import { formatCurrency } from '../utils/formatters';

const Optimization: React.FC = () => {
    const [filter, setFilter] = useState<'all' | 'aws' | 'azure'>('all');
    const [findings] = useState<OptimizationFinding[]>(sampleFindings);

    const filteredFindings = findings.filter(f => filter === 'all' || f.provider === filter);

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'high': return 'text-red-700 bg-red-50 border-red-200';
            case 'medium': return 'text-yellow-700 bg-yellow-50 border-yellow-200';
            case 'low': return 'text-blue-700 bg-blue-50 border-blue-200';
            default: return 'text-gray-700 bg-gray-50 border-gray-200';
        }
    };

    const getCategoryIcon = (category: string) => {
        switch (category) {
            case 'compute': return <Server className="h-4 w-4" />;
            case 'database': return <Database className="h-4 w-4" />;
            case 'storage': return <HardDrive className="h-4 w-4" />;
            default: return <AlertTriangle className="h-4 w-4" />;
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Optimization Hub</h1>
                    <p className="mt-1 text-sm text-gray-500">
                        Actionable recommendations to reduce cloud spend and improve efficiency.
                    </p>
                </div>

                <div className="flex items-center space-x-2">
                    <Filter className="h-4 w-4 text-gray-500" />
                    <select
                        className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                        value={filter}
                        onChange={(e) => setFilter(e.target.value as any)}
                    >
                        <option value="all">All Providers</option>
                        <option value="aws">AWS Only</option>
                        <option value="azure">Azure Only</option>
                    </select>
                </div>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
                    <h3 className="text-blue-100 font-medium text-sm">Total Potential Savings</h3>
                    <p className="text-3xl font-bold mt-2">
                        {formatCurrency(findings.reduce((acc, curr) => acc + curr.estimated_monthly_savings, 0))}
                    </p>
                    <p className="text-blue-100 text-sm mt-1">/ month</p>
                </div>

                <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
                    <h3 className="text-gray-500 font-medium text-sm">Open Opportunities</h3>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{findings.length}</p>
                    <p className="text-gray-500 text-sm mt-1">Across {filter === 'all' ? 'all clouds' : filter.toUpperCase()}</p>
                </div>

                <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
                    <h3 className="text-gray-500 font-medium text-sm">High Severity</h3>
                    <p className="text-3xl font-bold text-red-600 mt-2">
                        {findings.filter(f => f.severity === 'high').length}
                    </p>
                    <p className="text-gray-500 text-sm mt-1">Immediate action recommended</p>
                </div>
            </div>

            {/* Findings Table */}
            <div className="bg-white shadow-sm rounded-xl border border-gray-200 overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
                    <h3 className="text-lg font-medium text-gray-900">Optimization Findings</h3>
                </div>
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Severity
                                </th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Finding
                                </th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Resource
                                </th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Savings
                                </th>
                                <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {filteredFindings.map((finding) => (
                                <tr key={finding.id} className="hover:bg-gray-50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getSeverityColor(finding.severity)}`}>
                                            {finding.severity.toUpperCase()}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center">
                                            <div className={`p-2 rounded-lg mr-3 ${finding.provider === 'aws' ? 'bg-orange-100 text-orange-600' : 'bg-blue-100 text-blue-600'}`}>
                                                {getCategoryIcon(finding.category)}
                                            </div>
                                            <div>
                                                <div className="text-sm font-medium text-gray-900">{finding.description}</div>
                                                <div className="text-xs text-gray-500 capitalize">{finding.provider} • {finding.category}</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
                                        {finding.resource_id}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="text-sm font-bold text-green-600">
                                            {formatCurrency(finding.estimated_monthly_savings)}
                                        </div>
                                        <div className="text-xs text-gray-500">/ month</div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <button className="text-blue-600 hover:text-blue-900 flex items-center justify-end w-full group">
                                            Fix Now
                                            <ArrowRight className="ml-1 h-4 w-4 transform group-hover:translate-x-1 transition-transform" />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Optimization;
