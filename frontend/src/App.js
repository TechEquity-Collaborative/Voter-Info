import React, {Component} from 'react';
import SearchBar from './SearchBar'
import RepresentativeRow from './RepresentativeRow'
import {Jumbotron, Row, Col, Grid} from 'react-bootstrap'
import './App.css';
import scrollToComponent from 'react-scroll-to-component';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      results: [],
      address: null
    }
  }

  getResults = (address, lat, long) => {
    this.setState({
      address,
      results: ['hey', 'sup', 'yo', lat, long]
    }, () => scrollToComponent(this.resultsRow, {align: 'top'}))
  }

  render() {
    return (
      <React.Fragment>
        <Jumbotron className="jumbo-style">
          <Row style={{
            marginTop: '18%'
          }}>
            <Col md={6} mdOffset={3} sm={8} smOffset={2} xs={8} xsOffset={2}>
              <h2 style={{color: 'white'}}>
                FIND WHO REPRESENTS ME
              </h2>
              <p style={{color: 'white'}}>
                Get in touch with the elected officials that serve you. Enter your address below
                to find out who represents you.
              </p>
              <SearchBar onSelect={this.getResults}/>
            </Col>
          </Row>
        </Jumbotron>
        <Grid ref={(e) => this.resultsRow = e}>
          {this.state.address && this.state.results.length > 0 && <Row>
            <Col md={8} mdOffset={2}>
              <h1>My Representatives</h1>
              <p>These are the officials that serve {this.state.address}</p>
              {this
                .state
                .results
                .map((representative, i) => {
                  return <RepresentativeRow key={i} data={representative}/>
                })}
            </Col>
          </Row>
}
        </Grid>
      </React.Fragment>
    )
  }
}

export default App;
