// src/components/QuestionDetailPage.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // Import the useParams hook
import axios from 'axios';

function QuestionDetailPage() {
  const { id } = useParams(); // Extract the `id` parameter from the route
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [paragraphOrder, setParagraphOrder] = useState([]);

  useEffect(() => {
    const fetchQuestion = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/questions/${id}/`);
        setQuestion(response.data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching question details');
        setLoading(false);
      }
    };

    fetchQuestion();
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  // Handle RMMCQ option selection
  const handleOptionChange = (optionId) => {
    setSelectedOptions((prevOptions) =>
      prevOptions.includes(optionId)
        ? prevOptions.filter((id) => id !== optionId) // Unselect if already selected
        : [...prevOptions, optionId] // Select new option
    );
  };

  // Handle paragraph order input for RO
  const handleParagraphOrderChange = (e) => {
    setParagraphOrder(e.target.value.split(',').map((num) => parseInt(num.trim())));
  };

  // Submit user answers
  const handleSubmit = () => {
    console.log('User Answer:', userAnswer);
    console.log('Selected Options:', selectedOptions);
    console.log('Paragraph Order:', paragraphOrder);
    alert('Answer submitted successfully!');
  };

  return (
    <div>
      <h1>Question Detail</h1>
      <h2>{question.title}</h2>

      {/* RMMCQ */}
      {question.question_type === 'RMMCQ' && (
        <div>
          <p>{question.passage}</p>
          <h3>Options</h3>
          {question.options.map((option) => (
            <div key={option.id}>
              <input
                type="checkbox"
                id={`option-${option.id}`}
                value={option.id}
                checked={selectedOptions.includes(option.id)}
                onChange={() => handleOptionChange(option.id)}
              />
              <label htmlFor={`option-${option.id}`}>{option.content}</label>
            </div>
          ))}
        </div>
      )}

      {/* SST */}
      {question.question_type === 'SST' && (
        <div>
          <audio controls>
            <source src={question.audios} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
          <textarea
            placeholder="Type your answer here..."
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
          />
        </div>
      )}

      {/* RO */}
      {question.question_type === 'RO' && (
        <div>
          <p>Drag and drop paragraphs to reorder them:</p>
          {question.paragraphs.map((para, index) => (
            <div key={index}>
              {index + 1}. {para}
            </div>
          ))}
          <input
            type="text"
            placeholder="Enter the order (e.g., 3,1,2)"
            value={paragraphOrder.join(',')}
            onChange={handleParagraphOrderChange}
          />
        </div>
      )}

      <button onClick={handleSubmit}>Submit Answer</button>
    </div>
  );
}

export default QuestionDetailPage;
