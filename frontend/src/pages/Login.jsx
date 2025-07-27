import React, { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';

const ACCESS_CODES = {
    manager: import.meta.env.VITE_MANAGER_LOGIN,
    staff: import.meta.env.VITE_STAFF_LOGIN 
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

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(null);

        try {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/api/verify-code/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
          });

          const data = await response.json();

          if (response.ok && data.status === 'ok') {
              const now = new Date().getTime();
              localStorage.setItem('accessLevel', data.role);
              localStorage.setItem('sessionStart', now.toString());
              setAccessLevel(data.role);

              // Redirect based on role
              if (data.role === 'manager') {
                  navigate('/');
              } else if (data.role === 'staff') {
                  navigate('/orders');
              }
          } else {
              setError('Invalid access code.');
          }
        } catch (err) {
          console.error(err);
          setError('Invalid code')
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