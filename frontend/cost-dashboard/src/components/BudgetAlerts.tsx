/**
 * Budget Alerts Component
 * Displays budget alerts and warnings
 */

import React from 'react';
import {
  Box,
  Typography,
  Alert,
  AlertTitle,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider,
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  TrendingUp,
} from '@mui/icons-material';
import { BudgetAlert } from '../services/api';

interface BudgetAlertsProps {
  alerts: BudgetAlert[];
}

const BudgetAlerts: React.FC<BudgetAlertsProps> = ({ alerts }) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getAlertIcon = (alertType: string) => {
    switch (alertType) {
      case 'BUDGET_EXCEEDED':
        return <Error color="error" />;
      case 'SERVICE_BUDGET_EXCEEDED':
        return <Warning color="warning" />;
      default:
        return <Info color="info" />;
    }
  };

  const getAlertSeverity = (alertType: string): 'error' | 'warning' | 'info' => {
    switch (alertType) {
      case 'BUDGET_EXCEEDED':
        return 'error';
      case 'SERVICE_BUDGET_EXCEEDED':
        return 'warning';
      default:
        return 'info';
    }
  };

  const getAlertTitle = (alertType: string) => {
    switch (alertType) {
      case 'BUDGET_EXCEEDED':
        return 'Budget Exceeded';
      case 'SERVICE_BUDGET_EXCEEDED':
        return 'Service Budget Exceeded';
      default:
        return 'Budget Alert';
    }
  };

  if (alerts.length === 0) {
    return (
      <Box>
        <Alert severity="success" sx={{ mb: 2 }}>
          <AlertTitle>All Good!</AlertTitle>
          No budget alerts at this time. Your costs are within budget limits.
        </Alert>
        <Typography variant="body2" color="text.secondary" align="center">
          No active budget alerts
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Summary Alert */}
      <Alert severity={getAlertSeverity(alerts[0].alert_type)} sx={{ mb: 2 }}>
        <AlertTitle>{getAlertTitle(alerts[0].alert_type)}</AlertTitle>
        You have {alerts.length} active budget alert{alerts.length > 1 ? 's' : ''} requiring attention.
      </Alert>

      {/* Alerts List */}
      <List dense>
        {alerts.map((alert, index) => (
          <React.Fragment key={alert.id}>
            <ListItem sx={{ px: 0 }}>
              <ListItemIcon sx={{ minWidth: 40 }}>
                {getAlertIcon(alert.alert_type)}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2" fontWeight="medium">
                      {alert.service}
                    </Typography>
                    <Chip
                      label={`${formatCurrency(alert.current_cost)} / ${formatCurrency(alert.budget_limit)}`}
                      size="small"
                      color={alert.current_cost > alert.budget_limit ? 'error' : 'warning'}
                      variant="outlined"
                    />
                  </Box>
                }
                secondary={
                  <Box>
                    <Typography variant="caption" color="text.secondary">
                      {alert.message}
                    </Typography>
                    <Box display="flex" alignItems="center" mt={0.5}>
                      <TrendingUp sx={{ fontSize: 12, mr: 0.5 }} />
                      <Typography variant="caption" color="text.secondary">
                        {formatDate(alert.created_at)}
                      </Typography>
                    </Box>
                  </Box>
                }
              />
            </ListItem>
            {index < alerts.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </List>

      {/* Action Suggestion */}
      <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
        <Typography variant="subtitle2" gutterBottom>
          💡 Recommended Actions
        </Typography>
        <Typography variant="body2" color="text.secondary">
          • Review your AWS usage patterns
          • Consider right-sizing instances
          • Set up automated cost alerts
          • Implement cost allocation tags
        </Typography>
      </Box>
    </Box>
  );
};

export default BudgetAlerts;
