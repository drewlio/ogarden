import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import Container from 'react-bootstrap/Container';

import Navigation from './components/Navigation.js';
import ChartCard from './components/ChartCard.js';
import WeatherCard from './components/WeatherCard.js';


export default function App() {
  const [log, setLog] = useState([]);

  useEffect(() => {
    fetch('/api/log').then(res => res.json()).then(data => {
      setLog(Object.values(data));
    });
  }, []);
  

  return (
    <div>
      <Navigation />
        <Container>
          <ChartCard log={log} />
          <hr />
          <h2>History</h2>
          {log.reverse().map(l => <WeatherCard data={l} />)}
        </Container>
    </div>
  );
}

