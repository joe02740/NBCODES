import React, { useState } from 'react';

function SearchForm({ setResults }) {
  const [query, setQuery] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      console.log(`Sending request to: http://localhost:5000/search?q=${query}`);
      const response = await fetch(`http://localhost:5000/search?q=${query}`);
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Response data:', data);
      setResults(data);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  return (
    <form onSubmit={handleSearch} className="search-form">
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Enter search term"
      />
      <button type="submit" className="search-button">
        <img src="/images/Go-logo.png" alt="Search" />
      </button>
    </form>
  );
}

export default SearchForm;