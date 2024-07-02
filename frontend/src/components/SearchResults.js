import React, { useState } from 'react';
import ChatInterface from './ChatInterface';

function SearchResults({ results }) {
  const [selectedResult, setSelectedResult] = useState(null);

  const fetchAIExplanation = async (query, context) => {
    // ... your existing fetchAIExplanation function
  };

  const handleResultClick = async (result) => {
    const explanation = await fetchAIExplanation(result.Title, result.Content);
    setSelectedResult({ ...result, explanation });
  };

  if (!results) return null;

  return (
    <div className="search-results">
      {results.map((result, index) => (
        <div key={index} onClick={() => handleResultClick(result)}>
          <h3>{result.Title}</h3>
          <p>{result.Content.substring(0, 100)}...</p>
        </div>
      ))}
      {selectedResult && (
        <ChatInterface 
          initialContext={selectedResult.Content} 
          explanation={selectedResult.explanation} 
        />
      )}
    </div>
  );
}

export default SearchResults;