import React, { useState } from 'react';
import ChatInterface from './ChatInterface';

function SearchResults({ results }) {
  console.log('Search results:', results);
  const [explanations, setExplanations] = useState({});
  const [expandedResults, setExpandedResults] = useState({});
  const [chatOpen, setChatOpen] = useState({});

  const fetchAIExplanation = async (query, context) => {
    try {
      const response = await fetch('http://localhost:5000/ai_explain', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, context }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.explanation;
    } catch (error) {
      console.error("Error fetching AI explanation:", error);
      return "Unable to fetch explanation at this time.";
    }
  };

  const handleExplain = async (result) => {
    const explanation = await fetchAIExplanation(result.Title, result.Content);
    setExplanations(prev => ({ ...prev, [result.NodeId]: explanation }));
  };

  const toggleExpand = (nodeId) => {
    setExpandedResults(prev => ({
      ...prev,
      [nodeId]: !prev[nodeId]
    }));
  };

  const toggleChat = (nodeId) => {
    setChatOpen(prev => ({
      ...prev,
      [nodeId]: !prev[nodeId]
    }));
  };

  return (
    <div className="search-results">
      {results.length === 0 ? (
        <p>No results found for your search query.</p>
      ) : (
        results.map((result) => (
          <div key={result.NodeId} className="result-item">
            <h3>{result.Title}</h3>
            {result.Subtitle && <h4>{result.Subtitle}</h4>}
            <p>
              {expandedResults[result.NodeId] 
                ? result.Content 
                : `${result.Content.substring(0, 200)}...`}
            </p>
            <button onClick={() => toggleExpand(result.NodeId)}>
              {expandedResults[result.NodeId] ? 'Show Less' : 'Show More'}
            </button>
            <button onClick={() => handleExplain(result)}>Explain</button>
            {explanations[result.NodeId] && (
              <div className="explanation">
                <h4>AI Explanation:</h4>
                <p>{explanations[result.NodeId]}</p>
                <button onClick={() => toggleChat(result.NodeId)}>Follow Up</button>
              </div>
            )}
            {chatOpen[result.NodeId] && (
              <ChatInterface 
                initialContext={`${result.Title}\n${result.Subtitle ? result.Subtitle + '\n' : ''}${result.Content}`}
                explanation={explanations[result.NodeId]}
              />
            )}
          </div>
        ))
      )}
    </div>
  );
}

export default SearchResults;