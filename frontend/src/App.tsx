import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Recommendations from './pages/Recommendations';

const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/aws" element={<Dashboard />} />
            <Route path="/azure" element={<Dashboard />} />
            <Route path="/recommendations" element={<Recommendations />} />
          </Routes>
        </main>
        <footer className="bg-white border-t border-gray-200 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <p className="text-center text-gray-600 text-sm">
              Made with ❤️ in Nepal 🇳🇵 | CloudSathi - Cloud Cost Optimization
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
};

export default App;
