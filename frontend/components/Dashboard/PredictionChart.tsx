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
  predicted_value: number;
  lower_bound: number;
  upper_bound: number;
}

interface PredictionChartProps {
  data: PredictionData[];
  isLoading?: boolean;
}

const PredictionChart = ({ data, isLoading = false }: PredictionChartProps) => {
  console.log("PredictionChart", data);
  
  if (isLoading) {
    return <div className="h-96 flex items-center justify-center">Cargando predicciones...</div>;
  }

  return (
    <div className="w-full h-96 bg-white" style={{height: '200px'}}>
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
            dataKey="predicted_value"
            stroke="#8884d8"
            name="Predicción"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="lower_bound"
            stroke="#82ca9d"
            strokeDasharray="5 5"
            name="Límite Inferior"
          />
          <Line
            type="monotone"
            dataKey="upper_bound"
            stroke="#ffc658"
            strokeDasharray="5 5"
            name="Límite Superior"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionChart;