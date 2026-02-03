import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const Dashboard = () => {
    const [history, setHistory] = useState([]);
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const fetchHistory = async () => {
        try {
            const res = await api.get('history/');
            setHistory(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        setError(null);
        try {
            const res = await api.post('upload/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            // Navigate to summary of new dataset
            navigate(`/summary/${res.data.id}`);
        } catch (err) {
            setError('Upload failed. Check format.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Dashboard</h1>

            <div className="card">
                <h3>Upload New Dataset</h3>
                <form onSubmit={handleUpload}>
                    <input
                        type="file"
                        accept=".csv"
                        onChange={(e) => setFile(e.target.files[0])}
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? 'Uploading...' : 'Upload & Analyze'}
                    </button>
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                </form>
            </div>

            <h2>Recent Uploads</h2>
            <div className="card">
                {history.length === 0 ? <p>No uploads yet.</p> : (
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Uploaded At</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((item) => (
                                <tr key={item.id}>
                                    <td>{item.id}</td>
                                    <td>{new Date(item.uploaded_at).toLocaleString()}</td>
                                    <td>
                                        <button
                                            className="secondary"
                                            onClick={() => navigate(`/summary/${item.id}`)}
                                        >
                                            View Report
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
