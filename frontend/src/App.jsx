import { HashRouter as Router, Routes, Route, json } from 'react-router-dom';
import { useState } from 'react'
import Homepage from './modules/hompage';
import Testing from './modules/tesing_page';
import './App.css'

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route 
            path="/"
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
