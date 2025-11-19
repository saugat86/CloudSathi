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

    /**
     * Fetch top expensive resources from AWS CUR
     */
    async getTopResources(limit: number = 10): Promise<any[]> {
        if (USE_MOCK_DATA) {
            console.log('[Mock Data] Using sample CUR top resources');
            // Return mock data that matches the Athena result structure
            return [
                {
                    line_item_resource_id: "i-0a1b2c3d4e5f6g7h8",
                    line_item_product_code: "AmazonEC2",
                    line_item_usage_type: "RunInstances:SV006:t3.xlarge",
                    total_cost: "452.30",
                    line_item_currency_code: "USD"
                },
                {
                    line_item_resource_id: "vol-0x9y8z7a6b5c4d3e2",
                    line_item_product_code: "AmazonEC2",
                    line_item_usage_type: "EBS:VolumeUsage.gp2",
                    total_cost: "128.50",
                    line_item_currency_code: "USD"
                },
                {
                    line_item_resource_id: "arn:aws:rds:us-east-1:123:db:prod-db",
                    line_item_product_code: "AmazonRDS",
                    line_item_usage_type: "InstanceUsage:db.m5.large",
                    total_cost: "312.45",
                    line_item_currency_code: "USD"
                },
                {
                    line_item_resource_id: "nat-0a1b2c3d4e5f6g7h8",
                    line_item_product_code: "AmazonEC2",
                    line_item_usage_type: "NatGateway-Bytes",
                    total_cost: "89.20",
                    line_item_currency_code: "USD"
                },
                {
                    line_item_resource_id: "elb-prod-lb-123456789",
                    line_item_product_code: "AWSELB",
                    line_item_usage_type: "LoadBalancerUsage",
                    total_cost: "45.60",
                    line_item_currency_code: "USD"
                }
            ];
        }

        try {
            const response = await api.get('/api/aws/cur/top-resources', {
                params: { limit },
            });
            return response.data;
        } catch (error) {
            console.warn('[API Error] Failed to fetch CUR top resources', error);
            return [];
        }
    },

    /**
     * Fetch usage breakdown by operation from AWS CUR
     */
    async getUsageByOperation(limit: number = 10): Promise<any[]> {
        if (USE_MOCK_DATA) {
            return [
                { line_item_operation: "RunInstances", line_item_product_code: "AmazonEC2", total_cost: "850.20" },
                { line_item_operation: "PutObject", line_item_product_code: "AmazonS3", total_cost: "120.50" },
                { line_item_operation: "CreateDBInstance", line_item_product_code: "AmazonRDS", total_cost: "312.45" },
                { line_item_operation: "Invoke", line_item_product_code: "AWSLambda", total_cost: "45.30" },
                { line_item_operation: "GetObject", line_item_product_code: "AmazonS3", total_cost: "34.20" }
            ];
        }

        try {
            const response = await api.get('/api/aws/cur/usage-by-operation', {
                params: { limit },
            });
            return response.data;
        } catch (error) {
            console.warn('[API Error] Failed to fetch CUR usage by operation', error);
            return [];
        }
    }
};
