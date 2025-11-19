// TypeScript interfaces for cost data structures

export interface CostByService {
    service_name: string;
    amount: number;
    currency: string;
}

export interface CostByResourceGroup {
    resource_group: string;
    amount: number;
    currency: string;
}

export interface AWSCostResponse {
    start_date: string;
    end_date: string;
    total_cost: number;
    currency: string;
    costs_by_service: CostByService[];
}

export interface AzureCostResponse {
    start_date: string;
    end_date: string;
    total_cost: number;
    currency: string;
    costs_by_resource_group: CostByResourceGroup[];
    time_period_start: string;
    time_period_end: string;
}

export interface DateRange {
    startDate: string;
    endDate: string;
}
