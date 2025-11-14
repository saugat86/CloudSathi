import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import "tailwindcss/tailwind.css";
import { useToast } from "../utils/toast";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface CostData {
  date: string;
  [key: string]: any;
}

interface ServiceCost {
  service_name: string;
  amount: number;
  currency: string;
}

interface ResourceGroupCost {
  resource_group: string;
  amount: number;
  currency: string;
}

const API_MAP = {
  aws: "/api/aws/costs",
  azure: "/api/azure/costs",
};

type Provider = "aws" | "azure";

const today = new Date();
const weekAgo = new Date(today);
weekAgo.setDate(today.getDate() - 6);

function formatDate(date: Date) {
  return date.toISOString().slice(0, 10);
}

const CloudCostDashboard: React.FC = () => {
  const [provider, setProvider] = useState<Provider>("aws");
  const [startDate, setStartDate] = useState(formatDate(weekAgo));
  const [endDate, setEndDate] = useState(formatDate(today));
  const [loading, setLoading] = useState(false);
  const [costData, setCostData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const { showToast, Toast } = useToast();

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line
  }, [provider, startDate, endDate]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    setCostData(null);
    try {
      const url = `${API_MAP[provider]}?start_date=${startDate}&end_date=${endDate}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setCostData(data);
    } catch (e: any) {
      setError(e.message || "Failed to fetch data");
      showToast(e.message || "Failed to fetch data");
    } finally {
      setLoading(false);
    }
  };

  // Prepare chart data
  let chartLabels: string[] = [];
  let chartDatasets: any[] = [];
  if (costData) {
    if (provider === "aws" && costData.costs_by_service) {
      // Group by service, daily
      const serviceMap: Record<string, number[]> = {};
      chartLabels = [];
      // Simulate daily breakdown (if not present, just show total)
      costData.costs_by_service.forEach((svc: ServiceCost) => {
        serviceMap[svc.service_name] = [svc.amount];
      });
      chartLabels = [startDate];
      chartDatasets = Object.keys(serviceMap).map((svc, idx) => ({
        label: svc,
        data: serviceMap[svc],
        borderColor: `hsl(${(idx * 60) % 360}, 70%, 50%)`,
        backgroundColor: "rgba(0,0,0,0)",
      }));
    } else if (provider === "azure" && costData.costs_by_resource_group) {
      const rgMap: Record<string, number[]> = {};
      chartLabels = [];
      costData.costs_by_resource_group.forEach((rg: ResourceGroupCost) => {
        rgMap[rg.resource_group] = [rg.amount];
      });
      chartLabels = [startDate];
      chartDatasets = Object.keys(rgMap).map((rg, idx) => ({
        label: rg,
        data: rgMap[rg],
        borderColor: `hsl(${(idx * 60) % 360}, 70%, 50%)`,
        backgroundColor: "rgba(0,0,0,0)",
      }));
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4 text-center">Cloud Cost Dashboard</h2>
      <div className="flex flex-col md:flex-row gap-2 mb-4 items-center justify-center">
        <select
          className="border rounded px-2 py-1"
          value={provider}
          onChange={e => setProvider(e.target.value as Provider)}
        >
          <option value="aws">AWS</option>
          <option value="azure">Azure</option>
        </select>
        <input
          type="date"
          className="border rounded px-2 py-1"
          value={startDate}
          max={endDate}
          onChange={e => setStartDate(e.target.value)}
        />
        <span className="mx-1">to</span>
        <input
          type="date"
          className="border rounded px-2 py-1"
          value={endDate}
          min={startDate}
          max={formatDate(today)}
          onChange={e => setEndDate(e.target.value)}
        />
      </div>
      <Toast />
      {error && (
        <div className="bg-red-100 text-red-700 px-4 py-2 rounded mb-2 text-center">
          {error}
        </div>
      )}
      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : costData ? (
        <div className="bg-white rounded shadow p-4">
          <Line
            data={{ labels: chartLabels, datasets: chartDatasets }}
            options={{
              responsive: true,
              plugins: { legend: { position: "bottom" } },
              scales: { y: { beginAtZero: true } },
            }}
          />
          <div className="mt-4 text-sm text-gray-600 text-center">
            Total Cost: <span className="font-bold">{costData.total_cost} {costData.currency}</span>
          </div>
        </div>
      ) : (
        <div className="text-center text-gray-500">No data to display.</div>
      )}
    </div>
  );
};

export default CloudCostDashboard;
