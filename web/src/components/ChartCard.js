import React from 'react';
import { Line } from 'react-chartjs-2';

import Card from 'react-bootstrap/Card';
import { cToF } from '../logic/helpers.js';


export default function ChartCard({log}) {

  const temperature = [];
  log.map(l => temperature.push(cToF(l.ave_temperature)));

  const water = [];
  log.map(l => water.push(l.water_amount));

  // Convert the isodatetime's into Date objects
  const dates = [];
  log.map(l => dates.push(new Date(l.isodatetime)));

  // Convert the date objects into num days before now
  // (date subtraction returns milliseconds of time difference
  const days_ago = [];
  dates.map(d => days_ago.push((Date.now()-d)/1000/60/60/24));

  // fix precision to three 
  const days_ago_fixed = [];
  days_ago.map(d => days_ago_fixed.push(Number.parseFloat(d).toPrecision(3)));


  // Now we have our datasets to plot
  console.log(temperature);
  console.log(water);
  console.log(days_ago_fixed);


  const data = {
    labels: days_ago_fixed,
    datasets: [
      {
        label: 'Projected Temperature',
        data: temperature,
        borderColor: '#ff8a00',
        yAxisID: 'yAxisTemp',
      },
      {
        label: 'Water Applied',
        data: water,
        borderColor: '#006cff',
        yAxisID: 'yAxisWater',
      },
    ],
      
  };

  const options = {
    scales: {
      yAxisTemp: {
        position: 'left',
        suggestedMax: 40,
        suggestedMin: 0,
        title: {
          display: true,
          text: 'Projected Temperature (F)',
          color: '#ff8a00',
        },
      },
      yAxisWater: {
        position: 'right',
        suggestedMax: 10,
        suggestedMin: 0,
        title: {
          display: true,
          text: 'Water Applied (mm)',
          color: '#006cff',
        },
      },
    },
  };

  return (
    <div style={{ 'marginTop': '0.7rem' }}>
      <Card>
        <Card.Body>
          <Card.Title>
            <span>Previous {Math.round(Math.max(...days_ago_fixed))} days</span>
          </Card.Title>
          <Card.Text>
            <Line data={data} options={options} />
          </Card.Text>
        </Card.Body>
      </Card>

    </div>
  );

}

