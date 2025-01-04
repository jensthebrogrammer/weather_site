import { HashRouter as Router, Routes, Route, json } from 'react-router-dom';
import { useState, useEffect } from 'react'
import Homepage from './modules/hompage';
import Testing from './modules/tesing_page';
import './App.css'

function App() {
  // getting the data of the backend upon loading
  useEffect(() => {
    fetchData()
  }, [])  // the empty array is to make sure it loads only once

  const [backendData, setBackendData] = useState()

  const fetchData = async () => {
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

    setBackendData(data.data)

    console.log(data.message)
    console.log(backendData)
  }

  return (
    <>
    {/*using the router to route between pages*/}
      <Router>
        <Routes>
          <Route 
            path="/"
            // the loading page
            element={<Homepage />}
          />

          <Route 
            path="/testing_page"
            element={<Testing />}
          />
        </Routes>
      </Router>
    </>
  )
}

export default App
