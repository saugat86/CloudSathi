import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Optimization from './pages/Optimization';
import Recommendations from './pages/Recommendations'; // Keeping old page as "Cost Analyzer" placeholder or alternative

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/optimization" element={<Optimization />} />
          <Route path="/analyze" element={<Recommendations />} /> {/* Reusing Recommendations component as placeholder */}
          <Route path="/settings" element={<div className="p-4">Settings Page (Coming Soon)</div>} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
