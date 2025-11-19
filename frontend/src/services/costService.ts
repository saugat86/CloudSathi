import api from './api';
import { AWSCostResponse, AzureCostResponse } from '../types/cost';

export const costService = {
    /**
     * Fetch AWS cost data for a date range
     */
    async getAWSCosts(startDate: string, endDate: string): Promise<AWSCostResponse> {
        const response = await api.get<AWSCostResponse>('/api/aws/costs', {
            params: { start_date: startDate, end_date: endDate },
        });
        return response.data;
    },

    /**
     * Fetch Azure cost data for a date range
     */
    async getAzureCosts(startDate: string, endDate: string): Promise<AzureCostResponse> {
        const response = await api.get<AzureCostResponse>('/api/azure/costs', {
            params: { start_date: startDate, end_date: endDate },
        });
        return response.data;
    },
};
