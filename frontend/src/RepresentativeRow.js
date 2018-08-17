import React from 'react'
import {Row, Col, Image} from 'react-bootstrap';

let RepresentativeRow = (props) => {
  return (
    <Row className='result'>
      <Col xs={7}>
        <h2>City Representative</h2>
        <h3>John Doe</h3>
        <h3>123 Office Place</h3>
      </Col>
      <Col xs={4} xsOffset={1}>
        <Image src={'https://placehold.it/200x300'} responsive/>
      </Col>
    </Row>
  )
}

export default RepresentativeRow;