import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import SearchResults from './components/SearchResults';
import logo from './logo.png'; // Make sure this path is correct
import './App.css';

function App() {
  const [results, setResults] = useState(null);  // Initialize with null instead of []

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="New Bedford Seal" className="city-seal" />
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
      <a href="https://github.com/joe02740/NBCODES/blob/5b83e7492fcba59d1041d2d4be139a04a8a6b89b/frontend/README.md" className="contact-link">Readme</a>
      </footer>
    </div>
  );
}

export default App;