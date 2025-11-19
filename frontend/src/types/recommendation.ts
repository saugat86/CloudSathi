// TypeScript interfaces for recommendation data

export interface UsageData {
    EC2?: string;
    S3?: string;
    RDS?: string;
    Lambda?: string;
    [key: string]: string | undefined;
}

export interface RecommendationRequest {
    cost_data: UsageData;
}

export interface RecommendationResponse {
    recommendation: string;
}
