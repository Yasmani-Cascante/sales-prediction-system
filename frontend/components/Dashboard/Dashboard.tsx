'use client';

import React, { useState, useEffect } from 'react';
import PredictionChart from './PredictionChart';
import BranchSelector from './BranchSelector';
import MetricCard from './MetricCard';

const branches = [
  { id: 'Zurich', name: 'Zurich' },
  { id: 'Geneva', name: 'Geneva Lake View' },
  { id: 'Lausanne', name: 'Lausanne Main' },
];

const Dashboard = () => {
  const [selectedBranch, setSelectedBranch] = useState(branches[0].id);
  const [isLoading, setIsLoading] = useState(false);
  const [predictionData, setPredictionData] = useState([]);
  const [error, setError] = useState('');
  const [metrics, setMetrics] = useState({
    totalSales: 0,
    averageAccuracy: 0,
    trend: 0,
  });

  useEffect(() => {
    const fetchPredictions = async () => {
      setIsLoading(true);
      setError('');
      try {
        const response = await fetch(`http://localhost:8000/api/predict`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            branch_name: selectedBranch,
            periods: 30,
            frequency: "D"
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Error al obtener predicciones');
        }

        const data = await response.json();
        if (!data.predictions || !Array.isArray(data.predictions)) {
          throw new Error('Formato de datos inválido');
        }

        setPredictionData(data.predictions);
        console.log("Prediction Data:", data.predictions);
        
        if (data.metrics && data.model_performance) {
          setMetrics({
            totalSales: data.metrics.total_sales || 0,
            averageAccuracy: data.model_performance.accuracy || 0,
            trend: data.metrics.trend_percentage || 0,
          });
        }
      } catch (error) {
        console.error('Error:', error);
        setError(error.message);
        setPredictionData([]);
        setMetrics({
          totalSales: 0,
          averageAccuracy: 0,
          trend: 0,
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchPredictions();
  }, [selectedBranch]);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Dashboard de Predicción de Ventas
          </h1>
          <BranchSelector
            branches={branches}
            selectedBranch={selectedBranch}
            onBranchChange={setSelectedBranch}
          />
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <MetricCard
            title="Ventas Totales"
            value={metrics.totalSales}
            prefix="CHF "
            change={metrics.trend}
          />
          <MetricCard
            title="Precisión del Modelo"
            value={metrics.averageAccuracy}
            suffix="%"
          />
          <MetricCard
            title="Tendencia"
            value={metrics.trend}
            suffix="%"
            change={metrics.trend}
          />
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Predicción de Ventas
          </h2>
          <div className="aspect-[16/9] w-full">
            <PredictionChart data={predictionData} isLoading={isLoading} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;