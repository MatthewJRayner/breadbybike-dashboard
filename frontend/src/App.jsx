import { BrowserRouter as Router, Route, Routes, NavLink } from 'react-router-dom'
import Home from './pages/Home';
import Items from './pages/Items';
import Orders from './pages/Orders';
import Navbar from './components/Navbar';
import './App.css'

function App() {
  return (
    <Router>
      <div className='flex'>
        <Navbar />
        <div className='flex-col p-6 min-h-screen w-full'>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/items' element={<Items />} />
            <Route path='/orders' element={<Orders />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App
