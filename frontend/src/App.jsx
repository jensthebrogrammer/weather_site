import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Homepage from './modules/hompage';
import Testing from './modules/tesing_page';
import Loading_screen from './modules/loading_screen';
import './App.css';

function App() {
  // State for storing backend data
  const [backendData, setBackendData] = useState(() => {
    try {
      const storedData = localStorage.getItem('backendData')
      return storedData ? JSON.parse(storedData) : null
    } catch {
      localStorage.removeItem('backendData'); // remove corrupted data
      return {}
    }
  })
  

  // Effect to persist backendData to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('backendData', JSON.stringify(backendData));
  }, [backendData])

  // Key to trigger re-render of Homepage
  const [homeKey, setHomeKey] = useState(0);
  let page = <Loading_screen />

  // Fetch data from backend once on initial load
  useEffect(() => {
    fetchData()
  }, [])

  if (backendData) {
    page = <Homepage data={backendData} key={homeKey} />
    console.log(backendData)
  }

  const fetchData = async () => {
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // tells the server the request body is JSON
      },
      body: JSON.stringify({
        url: 'https://www.buienalarm.nl/belgie/arendonk/23100'
      }),
    }

    const url = 'http://127.0.0.1:5000/get_day_weather'
    const response = await fetch(url, options)
    const data = await response.json()

    setBackendData(data.data) // update React state
    setHomeKey(prev => prev + 1) // force Homepage to re-render with new data

    console.log(data)
  }

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={page}
        />
        <Route
          path="/testing_page"
          element={<Testing />}
        />
      </Routes>
    </Router>
  );
}

export default App;
