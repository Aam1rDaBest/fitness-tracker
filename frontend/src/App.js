import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Login from './pages/Login';
import PasswordResetForm from './pages/PasswordResetForm';
import PasswordResetRequest from './pages/PasswordResetReq';
import Protected from './pages/Protected';
import Signup from './pages/Signup';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/protected" element={<Protected />} />
        <Route path="/password-reset-request" element={<PasswordResetRequest />} />
        <Route path="/password-reset" element={<PasswordResetForm />} />
        {/* Add other routes here */}
      </Routes>
    </Router>
  );
}

export default App;