/**
 * Optimization Recommendations Component
 * Displays cost optimization recommendations
 */

import React from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider,
  Card,
  CardContent,
  Button,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Build,
  Speed,
  Security,
} from '@mui/icons-material';
import { OptimizationRecommendation } from '../services/api';

interface OptimizationRecommendationsProps {
  recommendations: OptimizationRecommendation[];
}

const OptimizationRecommendations: React.FC<OptimizationRecommendationsProps> = ({ recommendations }) => {
  const getPriorityColor = (priority: string): 'error' | 'warning' | 'info' | 'success' => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'success';
    }
  };

  const getImpactIcon = (impact: string) => {
    switch (impact.toLowerCase()) {
      case 'high':
        return <TrendingUp color="error" />;
      case 'medium':
        return <TrendingUp color="warning" />;
      case 'low':
        return <TrendingDown color="info" />;
      default:
        return <Build color="info" />;
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'right_sizing':
        return <Build color="primary" />;
      case 'instance_optimization':
        return <Speed color="primary" />;
      case 'security':
        return <Security color="primary" />;
      default:
        return <Build color="primary" />;
    }
  };

  const getTotalSavings = () => {
    return recommendations.reduce((total, rec) => {
      const savings = parseFloat(rec.potential_savings.replace('$', '').replace(',', ''));
      return total + savings;
    }, 0);
  };

  if (recommendations.length === 0) {
    return (
      <Box>
        <Typography variant="body2" color="text.secondary" align="center">
          No optimization recommendations available
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Summary Card */}
      <Card sx={{ mb: 2, bgcolor: 'primary.50' }}>
        <CardContent sx={{ py: 2 }}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="h6" color="primary">
                💰 Potential Savings
              </Typography>
              <Typography variant="h4" color="primary" fontWeight="bold">
                ${getTotalSavings().toLocaleString()}
              </Typography>
            </Box>
            <Box textAlign="right">
              <Typography variant="body2" color="text.secondary">
                {recommendations.length} recommendations
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Across {new Set(recommendations.map(r => r.service)).size} services
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Recommendations List */}
      <List dense>
        {recommendations.map((rec, index) => (
          <React.Fragment key={rec.id}>
            <ListItem sx={{ px: 0, alignItems: 'flex-start' }}>
              <Box sx={{ mr: 2, mt: 1 }}>
                {getCategoryIcon(rec.category)}
              </Box>
              <ListItemText
                primary={
                  <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
                    <Typography variant="body2" fontWeight="medium" sx={{ flex: 1 }}>
                      {rec.title}
                    </Typography>
                    <Box display="flex" gap={1}>
                      <Chip
                        label={rec.priority}
                        size="small"
                        color={getPriorityColor(rec.priority)}
                        variant="outlined"
                      />
                      <Chip
                        label={rec.potential_savings}
                        size="small"
                        color="success"
                        variant="filled"
                      />
                    </Box>
                  </Box>
                }
                secondary={
                  <Box>
                    <Typography variant="caption" color="text.secondary" display="block" mb={1}>
                      {rec.description}
                    </Typography>
                    <Box display="flex" alignItems="center" gap={2} mb={1}>
                      <Box display="flex" alignItems="center">
                        {getImpactIcon(rec.impact)}
                        <Typography variant="caption" sx={{ ml: 0.5 }}>
                          {rec.impact} impact
                        </Typography>
                      </Box>
                      <Typography variant="caption" color="text.secondary">
                        {rec.service} • {rec.category.replace('_', ' ')}
                      </Typography>
                    </Box>
                    <Typography variant="caption" color="primary" fontWeight="medium">
                      Action: {rec.action}
                    </Typography>
                  </Box>
                }
              />
            </ListItem>
            {index < recommendations.length - 1 && <Divider sx={{ my: 1 }} />}
          </React.Fragment>
        ))}
      </List>

      {/* Action Buttons */}
      <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
        <Button
          variant="contained"
          size="small"
          sx={{ flex: 1 }}
          onClick={() => {
            // TODO: Implement apply recommendations
            console.log('Apply recommendations');
          }}
        >
          Apply Recommendations
        </Button>
        <Button
          variant="outlined"
          size="small"
          onClick={() => {
            // TODO: Implement view details
            console.log('View details');
          }}
        >
          View Details
        </Button>
      </Box>
    </Box>
  );
};

export default OptimizationRecommendations;
