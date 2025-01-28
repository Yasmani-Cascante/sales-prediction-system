'use client';

import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface PredictionData {
  date: string;
  actual: number;
  predicted: number;
  lower_bound?: number;
  upper_bound?: number;
}

interface PredictionChartProps {
  data: PredictionData[];
  isLoading?: boolean;
}

const PredictionChart = ({ data, isLoading = false }: PredictionChartProps) => {
  if (isLoading) {
    return <div className="h-96 flex items-center justify-center">Cargando...</div>;
  }

  return (
    <div className="w-full h-96 bg-white p-4 rounded-lg shadow-lg">
      <ResponsiveContainer>
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="actual"
            stroke="#8884d8"
            name="Ventas Reales"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#82ca9d"
            name="Predicción"
            strokeWidth={2}
          />
          {data[0]?.lower_bound && (
            <Line
              type="monotone"
              dataKey="lower_bound"
              stroke="#82ca9d"
              strokeDasharray="5 5"
              name="Límite Inferior"
            />
          )}
          {data[0]?.upper_bound && (
            <Line
              type="monotone"
              dataKey="upper_bound"
              stroke="#82ca9d"
              strokeDasharray="5 5"
              name="Límite Superior"
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionChart;