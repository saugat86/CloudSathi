import React, { useState, useEffect } from 'react';
import {
    Table,
    Search,
    Download,
    Database,
    Cpu,
    HardDrive,
    Layers
} from 'lucide-react';
import { costService } from '../services/costService';
import { formatCurrency } from '../utils/formatters';
import LoadingSpinner from '../components/LoadingSpinner';

const CostAnalyzer: React.FC = () => {
    const [topResources, setTopResources] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const data = await costService.getTopResources(20);
                setTopResources(data);
            } catch (error) {
                console.error("Failed to fetch CUR data", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const getServiceIcon = (productCode: string) => {
        if (productCode.includes('EC2')) return <Cpu className="h-4 w-4 text-orange-500" />;
        if (productCode.includes('S3') || productCode.includes('EBS')) return <HardDrive className="h-4 w-4 text-green-500" />;
        if (productCode.includes('RDS') || productCode.includes('Dynamo')) return <Database className="h-4 w-4 text-blue-500" />;
        return <Layers className="h-4 w-4 text-gray-500" />;
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Cost Analyzer (CUR)</h1>
                    <p className="mt-1 text-sm text-gray-500">
                        Deep dive into AWS Cost and Usage Reports via Athena.
                    </p>
                </div>
                <button className="flex items-center px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">
                    <Download className="h-4 w-4 mr-2" />
                    Export CSV
                </button>
            </div>

            {/* Top Resources Table */}
            <div className="bg-white shadow-sm rounded-xl border border-gray-200 overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-200 bg-gray-50 flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900">Top Expensive Resources (Last 30 Days)</h3>
                    <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <Search className="h-4 w-4 text-gray-400" />
                        </div>
                        <input
                            type="text"
                            className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                            placeholder="Search resources..."
                        />
                    </div>
                </div>

                {loading ? (
                    <div className="p-12">
                        <LoadingSpinner message="Querying Athena..." />
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Service
                                    </th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Resource ID
                                    </th>
                                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Usage Type
                                    </th>
                                    <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Total Cost
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {topResources.map((resource, index) => (
                                    <tr key={index} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="flex items-center">
                                                <div className="mr-3 p-1.5 bg-gray-100 rounded-md">
                                                    {getServiceIcon(resource.line_item_product_code)}
                                                </div>
                                                <span className="text-sm font-medium text-gray-900">{resource.line_item_product_code}</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
                                            {resource.line_item_resource_id}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {resource.line_item_usage_type}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-bold text-gray-900">
                                            {formatCurrency(parseFloat(resource.total_cost))}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CostAnalyzer;
