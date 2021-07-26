import React from 'react';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import { cToF } from '../logic/helpers.js';


export default function WeatherCard({data}) {

  // Prepare data for displaying
  // This is the place to set precision and do unit conversion
  const d = {};

  d.date = new Date(data.isodatetime);
  const format = { dateStyle: 'full', timeStyle: 'short' };

  d.ave_temperature = Number.parseFloat(
                        cToF(data.ave_temperature)
                      ).toPrecision(3);

  d.ave_probability_of_precipitation = Math.round(
                                         data.ave_probability_of_precipitation);

  d.total_precipitation = data.total_precipitation.toFixed(1);

  d.ave_relative_humidity = Math.round(data.ave_relative_humidity);

  d.ave_sky_cover = Math.round(data.ave_sky_cover);

  d.ave_wind_gust = Number.parseFloat(
                      data.ave_wind_gust
                    ).toPrecision(2);

  d.ave_wind_speed = Number.parseFloat(
                       data.ave_wind_speed
                     ).toPrecision(2);

  d.sensor_value = Math.round(data.sensor_value);

  d.valve_duration = Math.round(data.valve_duration);

  d.water_amount = data.water_amount.toFixed(1);


  const measTitle = {
    'whiteSpace': 'noWrap',
  };


  const measValue = {
    'color': '#11844e',
    'fontWeight': 'bold',
    'whiteSpace': 'noWrap',
  };


  return (
    <div style={{ 'marginTop': '0.7rem' }}>
    <Card>
      <Card.Body>
        <Card.Title>
          {Intl.DateTimeFormat('en-US', format).format(d.date)}
        </Card.Title>
        <Card.Text>
         <Container>
           <Row xs={1} sm={2} md={3} lg={4}>
             <Col>
               <span style={measTitle}>Temperature </span>
               <span style={measValue}>{d.ave_temperature}&deg;F</span>
             </Col>
             <Col>
			   <span style={measTitle}>Precipitation </span>
               <span style={measValue}>{d.ave_probability_of_precipitation}% </span> 
             </Col>
             <Col>
               <span style={measTitle}>Precipitation Amount </span>
               <span style={measValue}>{d.total_precipitation}mm</span>
             </Col>
             <Col>
               <span style={measTitle}>Relative Humidity </span>
               <span style={measValue}>{d.ave_relative_humidity}% </span>
            </Col>
             <Col>
               <span style={measTitle}>Sky Cover </span>
               <span style={measValue}>{d.ave_sky_cover}% </span>
            </Col>
             <Col>
               <span style={measTitle}>Wind Gust </span>
               <span style={measValue}>{d.ave_wind_gust}kph </span>
            </Col>
             <Col>
               <span style={measTitle}>Wind Speed </span>
               <span style={measValue}>{d.ave_wind_speed}kph </span>
             </Col>
             <Col>
               <span style={measTitle}>Soil Moisture Sensor </span>
               <span style={measValue}>{d.sensor_value}% </span>
             </Col>
             <Col>
               <span style={measTitle}>Valve Duration </span>
               <span style={measValue}>{d.valve_duration}s </span>
             </Col>
             <Col>
               <span style={measTitle}>Water Applied </span>
               <span style={measValue}>{d.water_amount}mm </span>
             </Col>
           </Row>
         </Container>
        </Card.Text>
      </Card.Body>


    </Card>
    </div>
  );

}

