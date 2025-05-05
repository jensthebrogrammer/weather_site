import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Homepage from './modules/hompage';
import Testing from './modules/tesing_page';
import Loading_screen from './modules/loading_screen';
import { fetchData } from './scripts/usingData';
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
    fetchData(setBackendData, setHomeKey, "dessel")
  }, [])

  if (backendData) {
    page = (<Homepage
            data={backendData}
            key={homeKey} 
            setBackendData={setBackendData}
            setHomeKey={setHomeKey}
           />)
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
