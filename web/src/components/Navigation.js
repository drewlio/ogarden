import React, { useState, useEffect } from 'react';

import logo from './logo.svg';

import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';

export default function Navigation() {
  const [isValveOn, setIsValveOn] = useState(false);

  useEffect(() => {
    fetch('/api/valve').then(res => res.json()).then(data => {
      setIsValveOn(data.isValveOn);
      console.log(data);
    });
  }, []);


  const onSwitchAction = () => {
    const cmd = !isValveOn ? "on" : "off";
    fetch('/api/valve/' + cmd).then(res => res.json()).then(data => {
      setIsValveOn(data.isValveOn)
    });
  };


  return (
	<Navbar bg="light" expand="lg">
	  <Container>
		<Navbar.Brand href="#home">
          <img 
            src={logo} 
            width="30"
            height="30"
            className="d-inline-block align-top"
            style={ {"paddingRight": 10} }
            alt=""
          />
          Ogarden
        </Navbar.Brand>
		<Navbar.Toggle aria-controls="basic-navbar-nav" />
		<Navbar.Collapse id="basic-navbar-nav">
		  <Nav className="me-auto">
            <Navbar.Text>
              <Form>
{/* change to "switch" when bug is fixed */}
                <Form.Check
                  id="switch-1"
                  type="checkbox" 
                  label="Valve Control"
                  checked={isValveOn}
                  onChange={onSwitchAction}
                />
              </Form>
            </Navbar.Text>
		  </Nav>
		</Navbar.Collapse>
	  </Container>
	</Navbar>
  );
}

