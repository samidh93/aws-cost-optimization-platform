/**
 * Main Dashboard Component
 * Displays the cost optimization platform overview
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Alert,
  CircularProgress,
  Paper,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Warning,
  CheckCircle,
  AttachMoney,
  Timeline,
} from '@mui/icons-material';
import { apiService, HealthStatus, CostSummary, BudgetAlert, OptimizationRecommendation } from '../services/api';
import CostChart from './CostChart';
import BudgetAlerts from './BudgetAlerts';
import OptimizationRecommendations from './OptimizationRecommendations';
import ServiceBreakdown from './ServiceBreakdown';

const Dashboard: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [costSummary, setCostSummary] = useState<CostSummary | null>(null);
  const [budgetAlerts, setBudgetAlerts] = useState<BudgetAlert[]>([]);
  const [recommendations, setRecommendations] = useState<OptimizationRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch all dashboard data in parallel
        const [healthData, costData, alertsData, recommendationsData] = await Promise.all([
          apiService.getHealth(),
          apiService.getCostSummary(30),
          apiService.getBudgetAlerts(10),
          apiService.getOptimizationRecommendations(10),
        ]);

        setHealth(healthData);
        setCostSummary(costData);
        setBudgetAlerts(alertsData);
        setRecommendations(recommendationsData);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please check if the backend is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ ml: 2 }}>
          Loading dashboard...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  const getTrendIcon = (trendPercentage: number) => {
    return trendPercentage > 0 ? <TrendingUp color="error" /> : <TrendingDown color="success" />;
  };

  const getTrendColor = (trendPercentage: number) => {
    return trendPercentage > 0 ? 'error' : 'success';
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          🚀 Cost Optimization Platform
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Real-time AWS cost monitoring and optimization
        </Typography>
        
        {/* Health Status */}
        {health && (
          <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Chip
              icon={<CheckCircle />}
              label={`${health.status.toUpperCase()} - ${health.database}`}
              color={health.status === 'healthy' ? 'success' : 'error'}
              variant="outlined"
            />
            <Typography variant="body2" color="text.secondary">
              {health.data_counts.cost_records} cost records • {health.data_counts.budget_alerts} alerts • {health.data_counts.optimization_recommendations} recommendations
            </Typography>
          </Box>
        )}
      </Box>

      {/* Key Metrics */}
      {costSummary && (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
          <Box sx={{ flex: '1 1 250px', minWidth: '250px' }}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography color="text.secondary" gutterBottom>
                      Total Cost (30 days)
                    </Typography>
                    <Typography variant="h4" component="div">
                      ${costSummary.total_cost.toLocaleString()}
                    </Typography>
                  </Box>
                  <AttachMoney sx={{ fontSize: 40, color: 'primary.main' }} />
                </Box>
              </CardContent>
            </Card>
          </Box>

          <Box sx={{ flex: '1 1 250px', minWidth: '250px' }}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography color="text.secondary" gutterBottom>
                      Daily Average
                    </Typography>
                    <Typography variant="h4" component="div">
                      ${costSummary.daily_average.toLocaleString()}
                    </Typography>
                  </Box>
                  <Timeline sx={{ fontSize: 40, color: 'info.main' }} />
                </Box>
              </CardContent>
            </Card>
          </Box>

          <Box sx={{ flex: '1 1 250px', minWidth: '250px' }}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography color="text.secondary" gutterBottom>
                      Cost Trend
                    </Typography>
                    <Typography variant="h4" component="div" color={getTrendColor(costSummary.trend_percentage)}>
                      {costSummary.trend_percentage > 0 ? '+' : ''}{costSummary.trend_percentage.toFixed(1)}%
                    </Typography>
                  </Box>
                  {getTrendIcon(costSummary.trend_percentage)}
                </Box>
              </CardContent>
            </Card>
          </Box>

          <Box sx={{ flex: '1 1 250px', minWidth: '250px' }}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography color="text.secondary" gutterBottom>
                      Active Alerts
                    </Typography>
                    <Typography variant="h4" component="div" color={budgetAlerts.length > 0 ? 'error' : 'success'}>
                      {budgetAlerts.length}
                    </Typography>
                  </Box>
                  <Warning sx={{ fontSize: 40, color: budgetAlerts.length > 0 ? 'error.main' : 'success.main' }} />
                </Box>
              </CardContent>
            </Card>
          </Box>
        </Box>
      )}

      {/* Charts and Data */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        {/* Cost Trends Chart */}
        <Box sx={{ flex: '2 1 600px', minWidth: '600px' }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Cost Trends (Last 30 Days)
            </Typography>
            <CostChart />
          </Paper>
        </Box>

        {/* Service Breakdown */}
        <Box sx={{ flex: '1 1 300px', minWidth: '300px' }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Service Breakdown
            </Typography>
            <ServiceBreakdown />
          </Paper>
        </Box>

        {/* Budget Alerts */}
        <Box sx={{ flex: '1 1 400px', minWidth: '400px' }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Budget Alerts
            </Typography>
            <BudgetAlerts alerts={budgetAlerts} />
          </Paper>
        </Box>

        {/* Optimization Recommendations */}
        <Box sx={{ flex: '1 1 400px', minWidth: '400px' }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Optimization Recommendations
            </Typography>
            <OptimizationRecommendations recommendations={recommendations} />
          </Paper>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
