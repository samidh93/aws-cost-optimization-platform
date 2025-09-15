/**
 * API Service for Cost Optimization Platform
 * Handles all communication with the FastAPI backend
 */

import axios from 'axios';

// API base URL - points to our deployed AWS API Gateway
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://o4jbkndjo2.execute-api.us-east-1.amazonaws.com/prod';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types for our API responses
export interface CostData {
  id: number;
  account_id: string;
  timestamp: string;
  service: string;
  cost: number;
  total_daily_cost: number;
  processed_at: string;
  created_at: string;
}

export interface CostSummary {
  total_cost: number;
  daily_average: number;
  period_days: number;
  trend_percentage: number;
  service_breakdown: Array<{
    service: string;
    total_cost: number;
    percentage: number;
  }>;
}

export interface CostTrends {
  daily_costs: Array<{
    date: string;
    cost: number;
  }>;
  trend_direction: string;
  trend_percentage: number;
  period_days: number;
}

export interface BudgetAlert {
  id: number;
  account_id: string;
  timestamp: string;
  alert_type: string;
  service: string;
  current_cost: number;
  budget_limit: number;
  message: string;
  processed_at: string;
  created_at: string;
}

export interface OptimizationRecommendation {
  id: number;
  account_id: string;
  timestamp: string;
  recommendation_id: string;
  service: string;
  priority: string;
  category: string;
  title: string;
  description: string;
  potential_savings: string;
  action: string;
  impact: string;
  created_at: string;
}

export interface HealthStatus {
  status: string;
  service: string;
  version: string;
  database: string;
  data_counts: {
    cost_records: number;
    budget_alerts: number;
    optimization_recommendations: number;
  };
}

// API Service class
class ApiService {
  // Health endpoints
  async getHealth(): Promise<HealthStatus> {
    const response = await api.get('/health/detailed');
    return response.data;
  }

  // Cost data endpoints
  async getCostData(days: number = 7, service?: string): Promise<CostData[]> {
    const params = new URLSearchParams();
    params.append('days', days.toString());
    if (service) params.append('service', service);
    
    const response = await api.get(`/api/v1/cost/?${params.toString()}`);
    return response.data.data;
  }

  async getCostSummary(days: number = 30): Promise<CostSummary> {
    const response = await api.get(`/api/v1/cost/summary?days=${days}`);
    return response.data.summary;
  }

  async getCostTrends(days: number = 30): Promise<CostTrends> {
    const response = await api.get(`/api/v1/cost/trends?days=${days}`);
    return response.data.trends;
  }

  async getServicesBreakdown(days: number = 30): Promise<Array<{
    service: string;
    total_cost: number;
    average_cost: number;
    record_count: number;
    percentage: number;
  }>> {
    const response = await api.get(`/api/v1/cost/services?days=${days}`);
    return response.data.services;
  }

  // Budget endpoints
  async getBudgetAlerts(limit: number = 50, alertType?: string): Promise<BudgetAlert[]> {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    if (alertType) params.append('alert_type', alertType);
    
    const response = await api.get(`/api/v1/budget/?${params.toString()}`);
    return response.data.alerts;
  }

  async getBudgetSummary(): Promise<{
    total_alerts: number;
    recent_alerts: number;
    alerts_by_type: Array<{ type: string; count: number }>;
    alerts_by_service: Array<{ service: string; count: number }>;
  }> {
    const response = await api.get('/api/v1/budget/summary');
    return response.data.summary;
  }

  // Optimization endpoints
  async getOptimizationRecommendations(
    limit: number = 50,
    service?: string,
    priority?: string
  ): Promise<OptimizationRecommendation[]> {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    if (service) params.append('service', service);
    if (priority) params.append('priority', priority);
    
    const response = await api.get(`/api/v1/optimization/?${params.toString()}`);
    return response.data.recommendations;
  }

  async getOptimizationSummary(): Promise<{
    total_recommendations: number;
    total_potential_savings: string;
    recommendations_by_priority: Array<{ priority: string; count: number }>;
    recommendations_by_service: Array<{ service: string; count: number }>;
    recommendations_by_category: Array<{ category: string; count: number }>;
  }> {
    const response = await api.get('/api/v1/optimization/summary');
    return response.data.summary;
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;
