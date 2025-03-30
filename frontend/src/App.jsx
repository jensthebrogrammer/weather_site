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

  // setting the backend data
  // if there is stored data in the local storage, then it uses that. if it's empty (first load) then it just stores an empty object
  const [backendData, setBackendData] = useState(JSON.
    parse(localStorage.getItem('backendData')) || {})
  localStorage.setItem('backendData', JSON.stringify(backendData))

  // i'm giving the homepage a changable key here so i can reload the homepage without triggering useEffect
  const [homeKey, setHomeKey] = useState(0)

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

    // properly storing the backend data. local storage is used to ensure that upon reloading there is already data to be used
    setBackendData(data.data)
    localStorage.setItem('backendData', JSON.stringify(backendData))
    // making sure the site loads the new data
    setHomeKey(homeKey + 1) // changing the key triggers the reloading of the page

    console.log(data)
  }

  return (
    <>
    {/*using the router to route between pages*/}
      <Router>
        <Routes>
          <Route 
            path="/"
            // the loading page
            element={<Homepage data={backendData} key={homeKey}/>}
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
