import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import ConversationPage from './pages/ConversationPage';
import LandingPage from './pages/LandingPage';
import './App.css';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
`;

function App() {
  return (
    <AppContainer>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/conversation" element={<ConversationPage />} />
          <Route path="/conversation/:id" element={<ConversationPage />} />
        </Routes>
      </Router>
    </AppContainer>
  );
}

export default App;
