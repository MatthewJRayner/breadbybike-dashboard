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

  useEffect(() => {
    const stored = localStorage.getItem('accessLevel');
    setAccessLevel(stored);
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
        <div className='flex'>
          <Navbar />
          <div className='flex-col p-6 overflow-auto min-h-screen w-full'>
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
}

export default App
