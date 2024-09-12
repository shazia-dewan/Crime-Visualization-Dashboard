import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

function App() {
  const [pieChart, setPieChart] = useState(null);
  const [barChart, setBarChart] = useState(null);
  const [heatmap, setHeatmap] = useState(null);
  const [lineChart, setLineChart] = useState(null);

  useEffect(() => {
    const fetchCharts = async () => {
      try {
        const [pieResponse, barResponse, heatmapResponse, lineResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/plot/pie', { responseType: 'blob' }),
          axios.get('http://127.0.0.1:5000/api/plot/bar', { responseType: 'blob' }),
          axios.get('http://127.0.0.1:5000/api/plot/heatmap', { responseType: 'blob' }),
          axios.get('http://127.0.0.1:5000/api/plot/line', { responseType: 'blob' }),
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
    <Container className="App">
      <header className="App-header">
        <h1>Crime Visualization Dashboard</h1>
        <Button variant="primary" onClick={() => window.location.reload()}>
          Refresh Charts
        </Button>
      </header>
      <div className="charts-grid">
        <div className="chart-container">
          <Card className="chart-card">
            <Card.Body>
              <Card.Title>Pie Chart</Card.Title>
              {pieChart && <img src={pieChart} alt="Pie Chart" className="chart-image" />}
            </Card.Body>
          </Card>
        </div>
        <div className="chart-container">
          <Card className="chart-card">
            <Card.Body>
              <Card.Title>Bar Chart</Card.Title>
              {barChart && <img src={barChart} alt="Bar Chart" className="chart-image" />}
            </Card.Body>
          </Card>
        </div>
        <div className="chart-container">
          <Card className="chart-card">
            <Card.Body>
              <Card.Title>Heatmap</Card.Title>
              {heatmap && <img src={heatmap} alt="Heatmap" className="chart-image" />}
            </Card.Body>
          </Card>
        </div>
        <div className="chart-container">
          <Card className="chart-card">
            <Card.Body>
              <Card.Title>Line Chart</Card.Title>
              {lineChart && <img src={lineChart} alt="Line Chart" className="chart-image" />}
            </Card.Body>
          </Card>
        </div>
      </div>
      <footer className="App-footer">
        <p>© 2024 Crime Visualization Dashboard</p>
      </footer>
    </Container>
  );
}

export default App;






