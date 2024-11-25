// src/components/QuestionListPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function QuestionListPage() {
  const [questions, setQuestions] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [questionType, setQuestionType] = useState(''); // For filtering question type
  const [totalCount, setTotalCount] = useState(0); // Total number of questions
  const [pageSize, setPageSize] = useState(10); // Number of items per page (assumed from the API)

  useEffect(() => {
    const fetchQuestions = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/questions/`, {
          params: {
            question_type: questionType || undefined, // Send the filter if selected
            page: page,
          },
        });
        setQuestions(response.data.results);
        setTotalCount(response.data.count); // Set total question count
        setLoading(false);
      } catch (err) {
        setError('Error fetching questions');
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [page, questionType]); // Refetch whenever page or questionType changes

  const handleFilterChange = (type) => {
    setQuestionType(type); // Update the filter type
    setPage(1); // Reset to the first page when filter changes
  };

  const totalPages = Math.ceil(totalCount / pageSize); // Calculate total pages

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Question List</h1>

      {/* Filter Buttons */}
      <div>
        <button onClick={() => handleFilterChange('')} className={!questionType ? 'active-filter' : ''}>
          All
        </button>
        <button onClick={() => handleFilterChange('SST')} className={questionType === 'SST' ? 'active-filter' : ''}>
          Summarize Spoken Text (SST)
        </button>
        <button onClick={() => handleFilterChange('RMMCQ')} className={questionType === 'RMMCQ' ? 'active-filter' : ''}>
          Reading Multiple Choice Questions (RMMCQ)
        </button>
        <button onClick={() => handleFilterChange('RO')} className={questionType === 'RO' ? 'active-filter' : ''}>
          Re-Order Paragraphs (RO)
        </button>
      </div>

      {/* Table */}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Question Type</th>
          </tr>
        </thead>
        <tbody>
          {questions.map((question) => (
            <tr key={question.id}>
              <td>{question.id}</td>
              <td>{question.title}</td>
              <td>{question.question_type_display}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination */}
      <div>
        <button onClick={() => setPage(page - 1)} disabled={page === 1}>
          Previous
        </button>
        <button onClick={() => setPage(page + 1)} disabled={page === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
}

export default QuestionListPage;
