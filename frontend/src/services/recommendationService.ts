import api from './api';
import { RecommendationRequest, RecommendationResponse, UsageData } from '../types/recommendation';

export const recommendationService = {
    /**
     * Get AI-powered cost optimization recommendations
     */
    async getRecommendation(usageData: UsageData): Promise<RecommendationResponse> {
        const request: RecommendationRequest = {
            cost_data: usageData,
        };

        const response = await api.post<RecommendationResponse>('/api/recommendations', request);
        return response.data;
    },
};
