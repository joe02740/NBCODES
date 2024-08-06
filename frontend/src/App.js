import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import SearchResults from './components/SearchResults';
import { Link } from 'react-router-dom';
import logo from './logo.png';
import './App.css';

function App() {
  const [results, setResults] = useState(null);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="New Bedford Seal" className="city-seal" />
        <h1>New Bedford City Codes AI Search</h1>
      </header>
      <main>
        <section className="intro">
          <ul>
            <li>Welcome to the New Bedford City Codes Search Tool.</li>
            <li>Enter your query to search through city regulations and ordinances.</li>
            <li>After locating the code you're looking for, press "Explain" to have Claude AI explain the code.</li>
            <li>Press "Follow Up" to chat further with Claude AI about the subject.</li>
            <li><Link to="/table-of-contents">New Bedford Codes and Ordinances Table of Contents</Link></li>
          </ul>
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