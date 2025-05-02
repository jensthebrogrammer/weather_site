import React, { useState, useEffect } from 'react';
import RainGraph from './rain_graph';
import './App.css';

function App() {
  // Load stored data safely
  const [graphData, setGraphData] = useState(() => {
    const storedData = localStorage.getItem("graphData");
    return storedData ? JSON.parse(storedData) : [];
  });

  const [graphKey, setGraphKey] = useState(0);

  // Save to localStorage when data updates
  useEffect(() => {
    localStorage.setItem("graphData", JSON.stringify(graphData));
  }, [graphData]);

  const fetch_data = async () => {
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: 'https://www.buienalarm.nl/belgie/witgoor/2778415',
      }),
    };

    const url = 'http://127.0.0.1:5000/get_day_weather';

    try {
      const response = await fetch(url, options);
      const data = await response.json();

      if (data.data.today.graphString) {
        setGraphData(data.data.today.graphString);
        setGraphKey((prevKey) => prevKey + 1);
      }

      return data.data;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const buttonClicked = async () => {
    console.log("The button was clicked");

    const data = await fetch_data();
    console.log("Fetched Data:", data);
  };

  return (
    <>
      <div>
        <h1>{"This is a test"}</h1>
        <button onClick={buttonClicked}>Test this</button>
      </div>
      <RainGraph graphData={graphData} key={graphKey} />
    </>
  );
}

export default App;
