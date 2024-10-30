import axios from 'axios';
import lottie from "lottie-web";
import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import arrowAnimation from '../assets/Arrow right_custom_icon.json';
import '../css/auth.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [toggleAnimation, setToggleAnimation] = useState(false);
    const navigate = useNavigate();
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

    const handleTogglePassword = () => {
        setShowPassword(!showPassword);
        setToggleAnimation(true);
        setTimeout(() => setToggleAnimation(false), 300);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/tracker/login/', { username, password });
            localStorage.setItem('token', response.data.access);
            navigate('/protected');
        } catch (err) {
            setError('Invalid credentials');
        }
    };

    return (
        <div className="page">
            <header>
                <nav class="logo"></nav>
                <nav class="navigation">
                    <a href="">Home</a>
                    <a href="">Login</a>
                    <a href="">Signup</a>
                    <a href="">Re-roo</a>
                </nav>
            </header>
            <div className="login-background">
                <div className="form-container">
                    <h2>Login</h2>
                    {error && <p className="error">{error}</p>}
                    <form onSubmit={handleSubmit}>
                        <div class="input-box">
                            <label>Username:</label>
                            <span class="icon"><ion-icon name="person"></ion-icon></span>
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                                placeholder="Must include at least 5 characters"
                            />
                        </div>
                        <div class="input-box">
                            <label>Password:</label>
                            <span
                                className={`icon ${toggleAnimation ? "lock-toggle" : ""}`}
                                onClick={handleTogglePassword}
                                style={{ cursor: 'pointer' }}
                            >
                                <ion-icon name={showPassword ? "lock-open" : "lock-closed"}></ion-icon>
                            </span>
                            <input
                                type={showPassword ? "text" : "password"}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                placeholder="Must include at least 5 characters and be valid"
                            />
                        </div>
                        <button type="submit">
                            <span>Login</span>
                            <div ref={animationContainer} className="lottie-icon" />
                        </button>
                    </form>
                    <p className="text">Don't have an account? <a href="/signup">Sign up</a></p>
                    <p className="text">Forgot <a href="/password-reset-request">Password/ Username?</a></p>
                </div>
            </div>
        </div>
    );
};

export default Login;