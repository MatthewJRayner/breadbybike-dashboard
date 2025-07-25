import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'
import Home from './pages/Home';
import Items from './pages/Items';
import Orders from './pages/Orders';
import Login from './pages/Login';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import { updateCooldownCheck, triggerStatsUpdate } from './utils/updateStats';
import './App.css'

const App = () => {
  const [accessLevel, setAccessLevel] = useState(localStorage.getItem('accessLevel'));
  const SESSION_DURATION = 30 * 60 * 1000; // 30 Minutes in ms

  useEffect(() => {
    const storedAccess = localStorage.getItem('accessLevel');
    const sessionStart = parseInt(localStorage.getItem('sessionStart'), 10);
    const now = new Date().getTime();
    if (storedAccess && sessionStart && now - sessionStart < SESSION_DURATION) {
      setAccessLevel(storedAccess);
    } else {
      localStorage.removeItem('accessLevel');
      localStorage.removeItem('sessionStart');
      setAccessLevel(null);
    }
  }, []);

  useEffect(() => {
    if (!accessLevel) return;

    if (updateCooldownCheck()) {
      triggerStatsUpdate();
    }
  }, [accessLevel]);
    
  if (!accessLevel) {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login setAccessLevel={setAccessLevel} />} />
          <Route path="*" element={<Navigate to='/login' replace />} />
        </Routes>
      </Router>
    );
  }
  return (
    <Router>
      <div className='flex-col'>
        <div className='flex flex-col lg:flex-row'>
          <Navbar />
          <div className='flex-col p-4 overflow-auto min-h-screen w-full'>
            <Routes>
              <Route path='/' element={<Home />} />
              <Route path='/items' element={<Items />} />
              <Route path='/orders' element={<Orders />} />
              <Route path='/login' element={<Login setAccessLevel={setAccessLevel} />} />
              <Route path='*' element={<Navigate to='/' replace />}/>
            </Routes>
          </div>
        </div>
        <Footer />
      </div>
    </Router>
  );
};

export default App
