import React from 'react';
import CityCodeChat from './components/CityCodeChat';
import logo from './logo.png';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="New Bedford Seal" className="city-seal" />
        <h1>New Bedford City Codes Search</h1>
      </header>
      <main>
        <section className="intro">
          <p>Welcome to the New Bedford City Codes Search Tool. Ask any question about city regulations and ordinances.</p>
        </section>
        <CityCodeChat />
      </main>
      <footer>
        <a href="https://github.com/joe02740/NBCODES" className="contact-link">Readme</a>
      </footer>
    </div>
  );
}

export default App;