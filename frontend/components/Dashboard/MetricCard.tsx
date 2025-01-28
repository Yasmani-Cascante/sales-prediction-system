'use client';

import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: number | string;
  change?: number;
  prefix?: string;
  suffix?: string;
}

const MetricCard = ({ title, value, change, prefix = '', suffix = '' }: MetricCardProps) => {
  const isPositiveChange = change && change > 0;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      <div className="mt-2 flex items-baseline">
        <p className="text-2xl font-semibold text-gray-900">
          {prefix}{value}{suffix}
        </p>
        {change !== undefined && (
          <span
            className={`ml-2 flex items-center text-sm font-medium ${
              isPositiveChange ? 'text-green-600' : 'text-red-600'
            }`}
          >
            {isPositiveChange ? (
              <TrendingUp className="h-4 w-4 mr-1" />
            ) : (
              <TrendingDown className="h-4 w-4 mr-1" />
            )}
            {Math.abs(change)}%
          </span>
        )}
      </div>
    </div>
  );
};

export default MetricCard;