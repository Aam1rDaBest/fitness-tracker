import axios from 'axios';
import lottie from "lottie-web";
import React, { useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import arrowAnimation from '../assets/Arrow right_custom_icon.json';
import '../css/auth.css';

const PasswordResetForm = () => {
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errors, setErrors] = useState({});
    const [message, setMessage] = useState('');
    const [isTokenValid, setIsTokenValid] = useState(false);
    const [verificationNeeded, setVerificationNeeded] = useState(true);
    const animationContainer = useRef(null);
    const navigate = useNavigate();
    const location = useLocation();

    // Extract token from URL
    const token = new URLSearchParams(location.search).get('token');

    useEffect(() => {
        // Load animation
        const animation = lottie.loadAnimation({
            container: animationContainer.current, // The container that will hold the animation
            renderer: 'svg',
            loop: true,
            autoplay: true,
            animationData: arrowAnimation, // The animation JSON data
        });

        // Token verification logic
        const verifyToken = async () => {
            if (!verificationNeeded) return;

            try {
                const response = await axios.get(`http://localhost:8000/tracker/password-reset/verify/?token=${token}`);
                if (response.status === 200) {
                    setIsTokenValid(true);
                    setVerificationNeeded(false);
                } else {
                    setErrors({ general: 'Invalid or expired token' });
                }
            } catch (err) {
                setErrors({ general: 'Invalid or expired token' });
            }
        };

        verifyToken();

        // Cleanup on unmount
        return () => {
            animation.destroy();
        };
    }, [verificationNeeded, token]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            setErrors({ password: 'Passwords do not match' });
            return;
        }

        try {
            const response = await axios.post('http://localhost:8000/tracker/password-reset/confirm/', {
                token: token,
                password: password,
            });
            if (response.status === 200) {
                setMessage('Password has been reset successfully.');
                setTimeout(() => {
                    navigate('/login');
                    setVerificationNeeded(true);
                }, 1000);
            }
        } catch (err) {
            if (err.response?.data?.errors) {
                setErrors({ password: err.response.data.errors.password || 'Failed to reset password' });
            } else {
                setErrors({ general: 'Invalid or expired token' });
            }
        }
    };

    return (
        <div className="form-container">
            <h2>Reset Password</h2>
            {message && <p className="success-message">{message}</p>}
            {errors.general && <p className="error-message">{errors.general}</p>}
            {isTokenValid ? (
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>New Password:</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            placeholder="Enter new password"
                        />
                        {errors.password && <p className="error-message">{errors.password}</p>}
                    </div>
                    <div>
                        <label>Confirm Password:</label>
                        <input
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                            placeholder="Confirm new password"
                        />
                    </div>
                    <button type="submit">
                        <span>Reset Password</span>
                        <div ref={animationContainer} className="lottie-icon" />
                    </button>
                </form>
            ) : (
                <p>Verifying token...</p>
            )}
        </div>
    );
};

export default PasswordResetForm;