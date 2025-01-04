import React, { useState } from 'react';
import './App.css';

function App() {
  // fetch the data when btn clicked
  const buttonClicked = () => {
    console.log("the button was clicked");
    console.log(graphData)
    console.log(fetch_data())
  }

  const [graphData, setGraphData] = useState("")

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
    console.log(data.data[1])
    setGraphData(data.data[1])

    return data.data
  }

  return (
    <>
      <div>
        <h1>{"this is a test"}</h1>
        <button onClick={buttonClicked}>test this</button>
      </div>
      <div className="graph-container">
        <svg viewBox="0 0 370 200" xmlns="http://www.w3.org/2000/svg">
          <path
            className="line"
            d={"M0,200C0,200,6.667,200,10,200C13.333,200,16.667,200,20,200C23.333,200,26.667,200,30,200C33.333,200,36.667,200,40,200C43.333,200,46.667,200,50,200C53.333,200,56.667,200,60,200C63.333,200,66.667,200,70,200C73.333,200,76.667,200,80,200C83.333,200,86.667,202.217,90,200C93.333,197.783,96.667,192.25,100,186.7C103.333,181.15,106.667,176.7,110,166.7C113.333,156.7,116.667,138.933,120,126.7C123.333,114.467,126.667,102.2,130,93.3C133.333,84.4,136.667,75.517,140,73.3C143.333,71.083,146.667,77.767,150,80C153.333,82.233,156.667,82.25,160,86.7C163.333,91.15,166.667,103.367,170,106.7C173.333,110.033,176.667,107.817,180,106.7C183.333,105.583,186.667,100,190,100C193.333,100,196.667,102.25,200,106.7C203.333,111.15,206.667,122.267,210,126.7C213.333,131.133,216.667,131.083,220,133.3C223.333,135.517,230,140,230,140L230,200C230,200,223.333,200,220,200C216.667,200,213.333,200,210,200C206.667,200,203.333,200,200,200C196.667,200,193.333,200,190,200C186.667,200,183.333,200,180,200C176.667,200,173.333,200,170,200C166.667,200,163.333,200,160,200C156.667,200,153.333,200,150,200C146.667,200,143.333,200,140,200C136.667,200,133.333,200,130,200C126.667,200,123.333,200,120,200C116.667,200,113.333,200,110,200C106.667,200,103.333,200,100,200C96.667,200,93.333,200,90,200C86.667,200,83.333,200,80,200C76.667,200,73.333,200,70,200C66.667,200,63.333,200,60,200C56.667,200,53.333,200,50,200C46.667,200,43.333,200,40,200C36.667,200,33.333,200,30,200C26.667,200,23.333,200,20,200C16.667,200,13.333,200,10,200C6.667,200,0,200,0,200Z"}>
          </path>
        </svg>
      </div>
    </>
  );
}

export default App;
