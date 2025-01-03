import React from 'react';
import './App.css';

function App() {
  const buttonClicked = () => {
    console.log("the button was clicked");
    console.log(fetch_data())
  }

  const fetch_data = async () => {
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({url:'https://www.buienalarm.nl/belgie/arendonk/23100'})
    }
    const url = 'http://127.0.0.1:5000/get_day_weather'

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
