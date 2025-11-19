import api from './api';
import { AWSCostResponse, AzureCostResponse } from '../types/cost';
import { sampleAWSCosts, sampleAzureCosts, USE_MOCK_DATA } from './mockData';

export const costService = {
    /**
     * Fetch AWS cost data for a date range
     * Falls back to mock data if USE_MOCK_DATA is enabled or API fails
     */
    async getAWSCosts(startDate: string, endDate: string): Promise<AWSCostResponse> {
        if (USE_MOCK_DATA) {
            console.log('[Mock Data] Using sample AWS costs');
            return Promise.resolve(sampleAWSCosts);
        }

        try {
            const response = await api.get<AWSCostResponse>('/api/aws/costs', {
                params: { start_date: startDate, end_date: endDate },
            });
            return response.data;
        } catch (error) {
            console.warn('[API Error] Falling back to mock AWS data', error);
            return sampleAWSCosts;
        }
    },

    /**
     * Fetch Azure cost data for a date range
     * Falls back to mock data if USE_MOCK_DATA is enabled or API fails
     */
    async getAzureCosts(startDate: string, endDate: string): Promise<AzureCostResponse> {
        if (USE_MOCK_DATA) {
            console.log('[Mock Data] Using sample Azure costs');
            return Promise.resolve(sampleAzureCosts);
        }

        try {
            const response = await api.get<AzureCostResponse>('/api/azure/costs', {
                params: { start_date: startDate, end_date: endDate },
            });
            return response.data;
        } catch (error) {
            console.warn('[API Error] Falling back to mock Azure data', error);
            return sampleAzureCosts;
        }
    },
};
