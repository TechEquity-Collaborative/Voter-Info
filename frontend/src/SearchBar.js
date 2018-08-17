import React, { Component } from 'react';
import PlacesAutocomplete, { geocodeByAddress, getLatLng } from 'react-places-autocomplete';

/* eslint-disable react/prop-types */
const renderSuggestion = ({ formattedSuggestion }) => (
  <div>
    <strong>{formattedSuggestion.mainText}</strong>{' '}
    <small>{formattedSuggestion.secondaryText}</small>
  </div>
);

const shouldFetchSuggestions = ({ value }) => value.length > 2;

const onError = (status, clearSuggestions) => {
  console.log(
    'Error happened while fetching suggestions from Google Maps API',
    status
  );
  clearSuggestions();
};

class SearchBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      address: '',
      loading: false,
    };

    this.handleSelect = this.handleSelect.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleSelect(address) {
    this.setState({
      address,
      loading: true,
    });

    geocodeByAddress(address)
      .then(results => getLatLng(results[0]))
      .then(({ lat, lng }) => {
        this.props.onSelect(address, lat, lng)
        this.setState({
          loading: false,
        });
      })
      .catch(error => {
        console.log('Geocode Error', error); // eslint-disable-line no-console
        this.setState({
          loading: false,
        });
      });
  }

  handleChange(address) {
    this.setState({
      address,
    });
  }

  render() {
    const inputProps = {
      type: 'text',
      value: this.state.address,
      onChange: this.handleChange,
      autoFocus: true,
      placeholder: 'Enter address e.g. 123 Market St',
      name: 'Demo__input',
      id: 'my-input-id',
    };

    return (
      <div>
        <PlacesAutocomplete
          renderSuggestion={renderSuggestion}
          inputProps={inputProps}
          onSelect={this.handleSelect}
          onEnterKeyDown={this.handleSelect}
          onError={onError}
          shouldFetchSuggestions={shouldFetchSuggestions}
        />
        {this.state.loading && (
          <div>
            Loading...
          </div>
        )}
      </div>
    );
  }
}

export default SearchBar;
