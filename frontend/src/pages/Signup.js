import axios from 'axios';
import lottie from "lottie-web";
import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import arrowAnimation from '../assets/Arrow right_custom_icon.json';
import '../css/auth.css';

const Signup = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState({});
    const animationContainer = useRef(null);
    const navigate = useNavigate();

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
            await axios.post('http://localhost:8000/tracker/add_user/', { username, email, password });
            navigate('/login');
        } catch (err) {
            if (err.response && err.response.data && err.response.data.errors) {
                const errorData = err.response.data.errors;
                let formattedErrors = {};

                if (errorData.username) {
                    formattedErrors.username = errorData.username;
                }
                if (errorData.email) {
                    formattedErrors.email = errorData.email;
                }
                if (errorData.password) {
                    formattedErrors.password = errorData.password;
                }

                setErrors(formattedErrors);
            } else {
                setErrors({ general: 'Error creating account' });
            }
        }
    };

    return (
        <div className="form-container">
            <h2>Sign Up</h2>
            {errors.general && <p className="error-message">{errors.general}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        placeholder="Must include at least 5 characters"
                    />
                    {errors.username && <p className="error-message">{errors.username}</p>}
                </div>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        placeholder="Must be a valid email address"
                    />
                    {errors.email && <p className="error-message">{errors.email}</p>}
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        placeholder="Must include at least 5 characters and be valid"
                    />
                    {errors.password && <p className="error-message">{errors.password}</p>}
                </div>
                <button type="submit">
                    <span>Sign Up</span>
                    <div ref={animationContainer} className="lottie-icon" />
                </button>
            </form>
            <p>Already have an account? <a href="/login">Log in</a></p>
        </div>
    );
};

export default Signup;