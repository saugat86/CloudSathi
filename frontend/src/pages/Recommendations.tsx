import React, { useState } from 'react';
import { Lightbulb, Send, Sparkles } from 'lucide-react';
import { recommendationService } from '../services/recommendationService';
import { UsageData } from '../types/recommendation';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';

const Recommendations: React.FC = () => {
    const [usageData, setUsageData] = useState<UsageData>({
        EC2: '',
        S3: '',
        RDS: '',
        Lambda: '',
    });
    const [recommendation, setRecommendation] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleInputChange = (field: keyof UsageData, value: string) => {
        setUsageData(prev => ({ ...prev, [field]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // Filter out empty fields
        const filteredData: UsageData = {};
        Object.entries(usageData).forEach(([key, value]) => {
            if (value && value.trim()) {
                filteredData[key] = value;
            }
        });

        if (Object.keys(filteredData).length === 0) {
            setError('Please provide at least one service usage description');
            return;
        }

        try {
            setLoading(true);
            setError(null);
            setRecommendation(null);

            const result = await recommendationService.getRecommendation(filteredData);
            setRecommendation(result.recommendation);
        } catch (err: any) {
            const errorMessage = err.response?.data?.detail || 'Failed to get recommendations. Please try again.';
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-8">
                <div className="flex items-center">
                    <Sparkles className="h-8 w-8 text-yellow-500 mr-3" />
                    <h1 className="text-3xl font-bold text-gray-900">AI Cost Recommendations</h1>
                </div>
                <p className="mt-2 text-gray-600">
                    Describe your cloud service usage patterns to get AI-powered optimization recommendations
                </p>
            </div>

            {error && (
                <div className="mb-6">
                    <ErrorAlert message={error} onDismiss={() => setError(null)} />
                </div>
            )}

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                <form onSubmit={handleSubmit}>
                    <div className="space-y-4">
                        <div>
                            <label htmlFor="ec2" className="block text-sm font-medium text-gray-700 mb-1">
                                EC2 Usage
                            </label>
                            <input
                                type="text"
                                id="ec2"
                                value={usageData.EC2}
                                onChange={(e) => handleInputChange('EC2', e.target.value)}
                                placeholder="e.g., high usage, running 24/7, t2.micro instances"
                                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>

                        <div>
                            <label htmlFor="s3" className="block text-sm font-medium text-gray-700 mb-1">
                                S3 Usage
                            </label>
                            <input
                                type="text"
                                id="s3"
                                value={usageData.S3}
                                onChange={(e) => handleInputChange('S3', e.target.value)}
                                placeholder="e.g., infrequent access, large files, moderate usage"
                                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>

                        <div>
                            <label htmlFor="rds" className="block text-sm font-medium text-gray-700 mb-1">
                                RDS Usage
                            </label>
                            <input
                                type="text"
                                id="rds"
                                value={usageData.RDS}
                                onChange={(e) => handleInputChange('RDS', e.target.value)}
                                placeholder="e.g., MySQL database, low traffic, development environment"
                                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>

                        <div>
                            <label htmlFor="lambda" className="block text-sm font-medium text-gray-700 mb-1">
                                Lambda Usage
                            </label>
                            <input
                                type="text"
                                id="lambda"
                                value={usageData.Lambda}
                                onChange={(e) => handleInputChange('Lambda', e.target.value)}
                                placeholder="e.g., occasional triggers, short execution time"
                                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="mt-6 w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? (
                            <>
                                <Lightbulb className="animate-pulse h-5 w-5 mr-2" />
                                Generating Recommendations...
                            </>
                        ) : (
                            <>
                                <Send className="h-5 w-5 mr-2" />
                                Get Recommendations
                            </>
                        )}
                    </button>
                </form>
            </div>

            {loading && <LoadingSpinner message="AI is analyzing your usage patterns..." />}

            {recommendation && !loading && (
                <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg shadow-sm border-2 border-yellow-200 p-6">
                    <div className="flex items-start">
                        <Lightbulb className="h-6 w-6 text-yellow-600 mt-1 flex-shrink-0" />
                        <div className="ml-4">
                            <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                💡 Recommendation
                            </h3>
                            <p className="text-gray-800 leading-relaxed">{recommendation}</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Recommendations;
