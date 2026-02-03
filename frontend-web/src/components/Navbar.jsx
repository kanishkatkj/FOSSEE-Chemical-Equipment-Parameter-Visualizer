import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="brand">Chemical Visualizer</div>
            <div>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/">Login</Link>
            </div>
        </nav>
    );
};

export default Navbar;
