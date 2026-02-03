import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const Summary = () => {
    const { id } = useParams();
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get(`summary/${id}/`)
            .then(res => setData(res.data))
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    }, [id]);

    if (loading) return <div>Loading analysis...</div>;
    if (!data) return <div>Dataset not found.</div>;

    // Chart Data Preparation
    const typeChartData = {
        labels: data.type_distribution.map(d => d.equipment_type),
        datasets: [{
            label: 'Count',
            data: data.type_distribution.map(d => d.count),
            backgroundColor: ['#333333', '#666666', '#999999', '#cccccc', '#000000'],
        }]
    };

    const avgChartData = {
        labels: ['Flowrate', 'Pressure', 'Temperature'],
        datasets: [{
            label: 'Average Values',
            data: [data.averages.flowrate, data.averages.pressure, data.averages.temperature],
            backgroundColor: '#333333',
        }]
    };

    return (
        <div>
            <h1>Analysis Report: {data.file_name}</h1>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <p style={{ margin: 0 }}>Uploaded: {new Date(data.uploaded_at).toLocaleString()}</p>
                <button onClick={() => window.open(`http://localhost:8000/api/pdf/${id}/`, '_blank')}>Download PDF Report</button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
                <div className="card">
                    <h4>Total Items</h4>
                    <h2>{data.total_count}</h2>
                </div>
                <div className="card">
                    <h4>Avg Flowrate</h4>
                    <h2>{data.averages.flowrate}</h2>
                </div>
                <div className="card">
                    <h4>Avg Pressure</h4>
                    <h2>{data.averages.pressure}</h2>
                </div>
                <div className="card">
                    <h4>Avg Temperature</h4>
                    <h2>{data.averages.temperature}</h2>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
                <div className="card" style={{ height: '400px' }}>
                    <h3>Equipment Type Distribution</h3>
                    <div style={{ height: '300px', display: 'flex', justifyContent: 'center' }}>
                        <Pie data={typeChartData} options={{ maintainAspectRatio: false }} />
                    </div>
                </div>
                <div className="card" style={{ height: '400px' }}>
                    <h3>Parameter Averages</h3>
                    <div style={{ height: '300px' }}>
                        <Bar data={avgChartData} options={{ maintainAspectRatio: false, indexAxis: 'y' }} />
                    </div>
                </div>
            </div>

            <div className="card">
                <h3>Raw Data</h3>
                <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Type</th>
                                <th>Flowrate</th>
                                <th>Pressure</th>
                                <th>Temperature</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.data.map((item, idx) => (
                                <tr key={idx}>
                                    <td>{item.equipment_name}</td>
                                    <td>{item.equipment_type}</td>
                                    <td>{item.flowrate}</td>
                                    <td>{item.pressure}</td>
                                    <td>{item.temperature}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Summary;
