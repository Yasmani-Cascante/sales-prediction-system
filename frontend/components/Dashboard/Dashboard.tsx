'use client';

import React, { useState, useEffect } from 'react';
import PredictionChart from './PredictionChart';
import BranchSelector from './BranchSelector';
import MetricCard from './MetricCard';

const branches = [
  { id: 'zurich_central', name: 'Zurich Central' },
  { id: 'geneva_lake', name: 'Geneva Lake View' },
  { id: 'lausanne_main', name: 'Lausanne Main' },
];

const Dashboard = () => {
  const [selectedBranch, setSelectedBranch] = useState(branches[0].id);
  const [isLoading, setIsLoading] = useState(false);
  const [predictionData, setPredictionData] = useState([]);
  const [metrics, setMetrics] = useState({
    totalSales: 0,
    averageAccuracy: 0,
    trend: 0,
  });

  useEffect(() => {
    const fetchPredictions = async () => {
      setIsLoading(true);
      try {
        // TODO: Reemplazar con llamada real a la API
        const response = await fetch(`http://localhost:5000/predict`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            branch_name: selectedBranch,
            periods: 30,
          }),
        });

        if (!response.ok) {
          throw new Error('Error al obtener predicciones');
        }

        const data = await response.json();
        setPredictionData(data.predictions || []);
        
        // Actualizar métricas
        setMetrics({
          totalSales: data.total_sales || 0,
          averageAccuracy: data.accuracy || 0,
          trend: data.trend || 0,
        });
      } catch (error) {
        console.error('Error:', error);
        // TODO: Manejar el error apropiadamente
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
          <PredictionChart data={predictionData} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;