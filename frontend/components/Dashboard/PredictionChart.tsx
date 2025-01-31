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
  if (isLoading) {
    return (
      <div className="w-full min-h-[400px] flex items-center justify-center bg-gray-50">
        <div className="text-gray-500">Cargando predicciones...</div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="w-full min-h-[400px] flex items-center justify-center bg-gray-50">
        <div className="text-gray-500">No hay datos disponibles</div>
      </div>
    );
  }

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('es-ES', {
      month: 'short',
      day: 'numeric'
    });
  };

  const formatValue = (value: number) => {
    return `CHF ${value.toFixed(2)}`;
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border rounded shadow-lg">
          <p className="font-bold mb-2">{formatDate(label)}</p>
          {payload.map((item: any, index: number) => (
            <p key={index} className="flex items-center" style={{ color: item.color }}>
              <span className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: item.color }}></span>
              <span>{item.name}: {formatValue(item.value)}</span>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{ width: '100%', height: '400px' }}>
      <ResponsiveContainer>
        <LineChart
          data={data}
          margin={{
            top: 10,
            right: 30,
            left: 20,
            bottom: 10,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="date" 
            tickFormatter={formatDate}
            tick={{ fill: '#666' }}
            tickLine={{ stroke: '#666' }}
          />
          <YAxis 
            tickFormatter={formatValue}
            tick={{ fill: '#666' }}
            tickLine={{ stroke: '#666' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            verticalAlign="top"
            height={36}
          />
          <Line
            type="monotone"
            dataKey="predicted_value"
            stroke="#4f46e5"
            strokeWidth={2}
            name="Predicción"
            dot={false}
            activeDot={{ r: 6, fill: "#4f46e5" }}
          />
          <Line
            type="monotone"
            dataKey="lower_bound"
            stroke="#22c55e"
            strokeDasharray="5 5"
            name="Límite Inferior"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="upper_bound"
            stroke="#f97316"
            strokeDasharray="5 5"
            name="Límite Superior"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionChart;