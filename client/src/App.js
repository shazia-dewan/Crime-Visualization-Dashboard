import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [pieChart, setPieChart] = useState(null);
  const [barChart, setBarChart] = useState(null);
  const [heatmap, setHeatmap] = useState(null);
  const [lineChart, setLineChart] = useState(null);

  useEffect(() => {
    const fetchCharts = async () => {
      try {
        const [pieResponse, barResponse, heatmapResponse, lineResponse] = await Promise.all([
          axios.get('http://localhost:5000/api/plot/pie', { responseType: 'blob' }),
          axios.get('http://localhost:5000/api/plot/bar', { responseType: 'blob' }),
          axios.get('http://localhost:5000/api/plot/heatmap', { responseType: 'blob' }),
          axios.get('http://localhost:5000/api/plot/line', { responseType: 'blob' }),
        ]);

        setPieChart(URL.createObjectURL(pieResponse.data));
        setBarChart(URL.createObjectURL(barResponse.data));
        setHeatmap(URL.createObjectURL(heatmapResponse.data));
        setLineChart(URL.createObjectURL(lineResponse.data));
      } catch (error) {
        console.error('Error fetching charts:', error);
      }
    };

    fetchCharts();
  }, []);

  return (
    <div className="App">
      <h1>Crime Visualization Dashboard</h1>
      <div className="charts-grid">
        <div className="chart-container">
          <h2>Pie Chart</h2>
          {pieChart && <img src={pieChart} alt="Pie Chart" />}
        </div>
        <div className="chart-container">
          <h2>Bar Chart</h2>
          {barChart && <img src={barChart} alt="Bar Chart" />}
        </div>
        <div className="chart-container">
          <h2>Heatmap</h2>
          {heatmap && <img src={heatmap} alt="Heatmap" />}
        </div>
        <div className="chart-container">
          <h2>Line Chart</h2>
          {lineChart && <img src={lineChart} alt="Line Chart" />}
        </div>
      </div>
    </div>
  );
}

export default App;



