import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Protected = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        // Check if token exists in local storage
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login'); // Redirect to login page if not authenticated
        } else {
            setIsAuthenticated(true); // Set authentication status
        }
    }, [navigate]);

    if (!isAuthenticated) {
        return <div>Loading...</div>; // Show loading while checking authentication
    }

    return (
        <div>
            <h2>Protected Page</h2>
            <p>This is a protected page. Only visible to authenticated users.</p>
        </div>
    );
};

export default Protected;