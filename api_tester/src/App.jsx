import React from 'react';
import './App.css';

function App() {
  // fetch the data when btn clicked
  const buttonClicked = () => {
    console.log("the button was clicked");
    console.log(fetch_data())
  }

  // async function because we need to wait for the backend server
  const fetch_data = async () => {
    // giving the data that the backend needs
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // id don't even know what this does
      },
      body: JSON.stringify({url:'https://www.buienalarm.nl/belgie/arendonk/23100'})   // returning the data in the JSON format
    }

    // location of the backend
    const url = 'http://127.0.0.1:5000/get_day_weather'

    // getting the data from the backend
    const response = await fetch(url, options)
    const data = await response.json()
    console.log(data.message)

    return data.data
  }

  return (
    <div>
      <h1>{"this is a test"}</h1>
      <button onClick={buttonClicked}>test this</button>
    </div>
  );
}

export default App;
