import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from './components/Header';
import { StackExchangePage } from './pages/StackExchange';
import { Footer } from './components/Footer';
import { FlightsPage } from './pages/FlightsPage';

const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Header />
        <main className="flex-1 w-full">
          <Routes>
            <Route path="/" element={<StackExchangePage />} />
            <Route path="/vuelos" element={<FlightsPage />} />
            {/* Agregaremos las rutas para vuelos más adelante */}
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;