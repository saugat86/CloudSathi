// Sample/mock data for AWS and Azure costs
// Use this for development and demonstration when API is not available

import { AWSCostResponse, AzureCostResponse } from '../types/cost';

export const sampleAWSCosts: AWSCostResponse = {
    start_date: '2025-10-20',
    end_date: '2025-11-19',
    total_cost: 1247.85,
    currency: 'USD',
    costs_by_service: [
        {
            service_name: 'Amazon Elastic Compute Cloud',
            amount: 456.32,
            currency: 'USD',
        },
        {
            service_name: 'Amazon Simple Storage Service',
            amount: 234.18,
            currency: 'USD',
        },
        {
            service_name: 'Amazon Relational Database Service',
            amount: 312.45,
            currency: 'USD',
        },
        {
            service_name: 'AWS Lambda',
            amount: 89.67,
            currency: 'USD',
        },
        {
            service_name: 'Amazon CloudFront',
            amount: 78.23,
            currency: 'USD',
        },
        {
            service_name: 'Amazon DynamoDB',
            amount: 45.12,
            currency: 'USD',
        },
        {
            service_name: 'Amazon Elastic Load Balancing',
            amount: 31.88,
            currency: 'USD',
        },
    ],
};

export const sampleAzureCosts: AzureCostResponse = {
    start_date: '2025-10-20',
    end_date: '2025-11-19',
    total_cost: 892.45,
    currency: 'USD',
    costs_by_resource_group: [
        {
            resource_group: 'production-rg',
            amount: 423.67,
            currency: 'USD',
        },
        {
            resource_group: 'development-rg',
            amount: 198.34,
            currency: 'USD',
        },
        {
            resource_group: 'staging-rg',
            amount: 156.89,
            currency: 'USD',
        },
        {
            resource_group: 'testing-rg',
            amount: 78.45,
            currency: 'USD',
        },
        {
            resource_group: 'shared-services-rg',
            amount: 35.10,
            currency: 'USD',
        },
    ],
    time_period_start: '2025-10-20',
    time_period_end: '2025-11-19',
};

// Flag to enable/disable mock data
export const USE_MOCK_DATA = process.env.REACT_APP_USE_MOCK_DATA === 'true';
