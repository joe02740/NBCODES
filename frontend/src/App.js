import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import SearchResults from './components/SearchResults';
import './App.css';

function App() {
  const [results, setResults] = useState([]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>New Bedford City Codes Search</h1>
      </header>
      <main>
        <section className="intro">
          <p>Welcome to the New Bedford City Codes Search Tool. Enter your query to search through city regulations and ordinances.</p>
        </section>
        <SearchForm setResults={setResults} />
        <SearchResults results={results} />
      </main>
      <footer>
        <p>&copy; 2024 City of New Bedford</p>
      </footer>
    </div>
  );
}

export default App;