// Sample/mock data for AWS and Azure costs
// Use this for development and demonstration when API is not available

import { AWSCostResponse, AzureCostResponse } from '../types/cost';

// Helper to generate daily data
const generateDailyCosts = (days: number, baseAmount: number, variance: number) => {
    const data = [];
    const today = new Date();
    for (let i = days; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const amount = baseAmount + (Math.random() * variance * 2 - variance);
        data.push({
            date: date.toISOString().split('T')[0],
            amount: Number(amount.toFixed(2)),
        });
    }
    return data;
};

export const sampleAWSCosts: AWSCostResponse & { daily_costs: any[] } = {
    start_date: '2025-10-20',
    end_date: '2025-11-19',
    total_cost: 1247.85,
    currency: 'USD',
    costs_by_service: [
        { service_name: 'Amazon Elastic Compute Cloud', amount: 456.32, currency: 'USD' },
        { service_name: 'Amazon Simple Storage Service', amount: 234.18, currency: 'USD' },
        { service_name: 'Amazon Relational Database Service', amount: 312.45, currency: 'USD' },
        { service_name: 'AWS Lambda', amount: 89.67, currency: 'USD' },
        { service_name: 'Amazon CloudFront', amount: 78.23, currency: 'USD' },
        { service_name: 'Amazon DynamoDB', amount: 45.12, currency: 'USD' },
        { service_name: 'Amazon Elastic Load Balancing', amount: 31.88, currency: 'USD' },
    ],
    daily_costs: generateDailyCosts(30, 42, 15), // Avg $42/day
};

export const sampleAzureCosts: AzureCostResponse & { daily_costs: any[] } = {
    start_date: '2025-10-20',
    end_date: '2025-11-19',
    total_cost: 892.45,
    currency: 'USD',
    costs_by_resource_group: [
        { resource_group: 'production-rg', amount: 423.67, currency: 'USD' },
        { resource_group: 'development-rg', amount: 198.34, currency: 'USD' },
        { resource_group: 'staging-rg', amount: 156.89, currency: 'USD' },
        { resource_group: 'testing-rg', amount: 78.45, currency: 'USD' },
        { resource_group: 'shared-services-rg', amount: 35.10, currency: 'USD' },
    ],
    time_period_start: '2025-10-20',
    time_period_end: '2025-11-19',
    daily_costs: generateDailyCosts(30, 28, 10), // Avg $28/day
};

// Detailed FinOps Recommendations
export interface OptimizationFinding {
    id: string;
    severity: 'high' | 'medium' | 'low';
    category: 'compute' | 'storage' | 'database' | 'network';
    provider: 'aws' | 'azure';
    resource_id: string;
    description: string;
    estimated_monthly_savings: number;
    status: 'open' | 'ignored' | 'fixed';
}

export const sampleFindings: OptimizationFinding[] = [
    {
        id: 'opt-001',
        severity: 'high',
        category: 'compute',
        provider: 'aws',
        resource_id: 'i-0a1b2c3d4e5f6g7h8',
        description: 'Idle EC2 Instance (t3.xlarge) - < 5% CPU for 7 days',
        estimated_monthly_savings: 124.80,
        status: 'open',
    },
    {
        id: 'opt-002',
        severity: 'high',
        category: 'storage',
        provider: 'aws',
        resource_id: 'vol-0x9y8z7a6b5c4d3e2',
        description: 'Unattached EBS Volume (500 GB gp2)',
        estimated_monthly_savings: 50.00,
        status: 'open',
    },
    {
        id: 'opt-003',
        severity: 'medium',
        category: 'database',
        provider: 'azure',
        resource_id: 'sql-prod-db-01',
        description: 'Over-provisioned SQL Database - Consider scaling down to Standard S2',
        estimated_monthly_savings: 75.50,
        status: 'open',
    },
    {
        id: 'opt-004',
        severity: 'low',
        category: 'network',
        provider: 'aws',
        resource_id: 'eipalloc-12345678',
        description: 'Unassociated Elastic IP Address',
        estimated_monthly_savings: 3.50,
        status: 'open',
    },
    {
        id: 'opt-005',
        severity: 'medium',
        category: 'compute',
        provider: 'azure',
        resource_id: 'vm-dev-02',
        description: 'Development VM running on weekends',
        estimated_monthly_savings: 45.00,
        status: 'open',
    },
];

export const sampleBudget = {
    total_budget: 2500,
    current_spend: 2140.30, // AWS + Azure
    forecasted_spend: 2650.00,
    alert_threshold: 80, // %
};

// Flag to enable/disable mock data
export const USE_MOCK_DATA = process.env.REACT_APP_USE_MOCK_DATA === 'true';
