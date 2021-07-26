import React, { useState, useEffect } from 'react';

import useInterval from '../hooks/useInterval.js';

import logo from './logo.svg';

import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';


export default function Sensor() {
  const [sensorValue, setSensorValue] = useState(null);

  function fetchRandom() {
    fetch('/api/random').then(res => res.json()).then(data => {
      setSensorValue(data.random);
      console.log(data.random);
    });
  }


  useInterval(() => {
    fetchRandom();
  }, 1000);

  useEffect(() => {
    fetchRandom();
    
    //fetch('/api/sensor').then(res => res.json()).then(data => {
    //  setSensorValue(data.sensor_value);
    //});
  }, []);

  return (
    <div style={{ 'marginTop': '0.7rem' }}>
    <Card>
      <Card.Body>
        <Card.Title>Soil Moisture Sensor</Card.Title>
        <Card.Text>
          Current value: {sensorValue}
        </Card.Text>
      </Card.Body>


    </Card>
    </div>
  );

}

