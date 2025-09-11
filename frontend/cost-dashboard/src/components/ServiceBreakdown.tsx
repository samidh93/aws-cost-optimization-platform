/**
 * Service Breakdown Component
 * Displays cost breakdown by AWS service using a pie chart
 */

import React, { useState, useEffect } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import { Box, Typography, List, ListItem, ListItemText, Chip } from '@mui/material';
import { apiService } from '../services/api';

interface ServiceData {
  service: string;
  total_cost: number;
  average_cost: number;
  record_count: number;
  percentage: number;
}

const ServiceBreakdown: React.FC = () => {
  const [services, setServices] = useState<ServiceData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        setLoading(true);
        setError(null);
        const servicesData = await apiService.getServicesBreakdown(30);
        setServices(servicesData);
      } catch (err) {
        console.error('Error fetching services breakdown:', err);
        setError('Failed to load services breakdown');
      } finally {
        setLoading(false);
      }
    };

    fetchServices();
  }, []);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  // Colors for the pie chart
  const COLORS = [
    '#1976d2', // Blue
    '#388e3c', // Green
    '#f57c00', // Orange
    '#d32f2f', // Red
    '#7b1fa2', // Purple
    '#00796b', // Teal
    '#5d4037', // Brown
    '#455a64', // Blue Grey
  ];

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={300}>
        <Typography>Loading breakdown...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={300}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!services || services.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={300}>
        <Typography color="text.secondary">No service data available</Typography>
      </Box>
    );
  }

  // Prepare data for the pie chart
  const chartData = services.map((service, index) => ({
    name: service.service,
    value: service.total_cost,
    percentage: service.percentage,
    color: COLORS[index % COLORS.length],
  }));

  return (
    <Box>
      {/* Pie Chart */}
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name }) => name}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value: number) => [formatCurrency(value), 'Cost']}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #ccc',
              borderRadius: '4px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            }}
          />
        </PieChart>
      </ResponsiveContainer>

      {/* Service List */}
      <Box sx={{ mt: 2 }}>
        <Typography variant="subtitle2" gutterBottom>
          Service Details
        </Typography>
        <List dense>
          {services.map((service, index) => (
            <ListItem key={service.service} sx={{ px: 0 }}>
              <Box
                sx={{
                  width: 12,
                  height: 12,
                  backgroundColor: COLORS[index % COLORS.length],
                  borderRadius: '50%',
                  mr: 1,
                  mt: 0.5,
                }}
              />
              <ListItemText
                primary={
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2" fontWeight="medium">
                      {service.service}
                    </Typography>
                    <Chip
                      label={formatCurrency(service.total_cost)}
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                }
                secondary={
                  <Typography variant="caption" color="text.secondary">
                    {service.percentage.toFixed(1)}% • {service.record_count} records
                  </Typography>
                }
              />
            </ListItem>
          ))}
        </List>
      </Box>
    </Box>
  );
};

export default ServiceBreakdown;
