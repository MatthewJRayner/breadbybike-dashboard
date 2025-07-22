import React, { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';

const ACCESS_CODES = {
    manager: 'FW42',
    staff: 'HIPPY41'
}

const Login = ({ setAccessLevel }) => {
    const [code, setCode] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const now = new Date().getTime();
    localStorage.setItem('sessionStart', now.toString());
    const accessLevel = localStorage.getItem('accessLevel');

    if (accessLevel === 'manager') return <Navigate to='/' replace />;
    if (accessLevel === 'staff') return <Navigate to='/orders' replace />;

    const handleLogin = (e) => {
        e.preventDefault();
        const now = new Date().getTime();

        if (code === ACCESS_CODES.manager) {
            localStorage.setItem('accessLevel', 'manager');
            localStorage.setItem('sessionStart', now.toString());
            setAccessLevel('manager');
            navigate('/');
        } else if (code === ACCESS_CODES.staff) {
            localStorage.setItem('accessLevel', 'staff');
            localStorage.setItem('sessionStart', now.toString());
            setAccessLevel('staff');
            navigate('/orders');
        } else {
            setError('Invalid access code.');
        }
    };

    return (
    <div className="flex flex-col items-center justify-center h-screen">
      <form onSubmit={handleLogin} className="p-6 bg-white shadow-md rounded-md">
        <h1 className="text-xl font-bold mb-4 text-black_text">Enter Access Code</h1>
        <input
          type="password"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="border border-bbb-blue-500 p-2 rounded w-full mb-3"
          placeholder="Access Code"
        />
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <button type="submit" className="bg-bbb-blue-500 hover:bg-bbb-blue-700 text-white px-4 py-2 rounded">
          Enter
        </button>
      </form>
    </div>
  );
};

export default Login;