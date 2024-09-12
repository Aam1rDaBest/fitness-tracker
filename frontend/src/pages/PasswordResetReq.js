import axios from 'axios';
import lottie from "lottie-web";
import React, { useEffect, useRef, useState } from 'react';
import arrowAnimation from '../assets/Arrow right_custom_icon.json';
import '../css/auth.css';

const PasswordResetRequest = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const animationContainer = useRef(null);

    useEffect(() => {
        const animation = lottie.loadAnimation({
            container: animationContainer.current, // The container that will hold the animation
            renderer: 'svg',
            loop: true,
            autoplay: true,
            animationData: arrowAnimation, // The animation JSON data
        });

        return () => {
            animation.destroy(); // Cleanup on unmount
        };
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/tracker/password-reset/', { email });
            setMessage(response.data.message); // Show success message
            setError(''); // Clear any previous error
        } catch (err) {
            setError('An error occurred. Please try again.');
            setMessage('');
        }
    };

    return (
        <div className="form-container">
            <h2>Reset Password</h2>
            <h3 className='sub-header'>Get Username + Password Reset Link</h3>
            {message && <p className="success-message">{message}</p>}
            {error && <p className="error-message">{error}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        placeholder="Enter your email address"
                    />
                </div>
                <button type="submit">
                    <span>Request Reset Link</span>
                    <div ref={animationContainer} className="lottie-icon" />
                </button>
            </form>
            <p>Already have an account? <a href="/login">Log in</a></p>
            <p>Don't have an account? <a href="/signup">Sign up</a></p>
        </div>
    );
};

export default PasswordResetRequest;



