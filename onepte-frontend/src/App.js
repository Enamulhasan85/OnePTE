// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import QuestionListPage from './components/QuestionListPage'; // Correct the duplicate import
import QuestionDetailPage from './components/QuestionDetailPage'; // Import the QuestionDetailPage component

function App() {
  return (
    <Router>
      <Routes>
        {/* Route for the list of questions */}
        <Route path="/questions" element={<QuestionListPage />} />
        {/* Route for question detail page */}
        <Route path="/questions/:id" element={<QuestionDetailPage />} />
      </Routes>
    </Router>
  );
}

export default App;
