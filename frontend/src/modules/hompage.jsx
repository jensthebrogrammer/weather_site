import React from "react";
import { Link } from "react-router-dom";
import GridBar from "./gridBar";
import { useState } from "react";
import { fetchData } from "../scripts/usingData";

import "/Users/35257/PycharmProjects/weather_app/frontend/src/App.css"


export default function Homepage({data, setBackendData, setHomeKey}) {
  // this code is expirimental. i'm generating html using js
  const navBarBtns = ["", '', ""]
  const [inputVal, SetInputVal] = useState("")
  
  const onSubmit = (e) => {
    e.preventDefault()
    console.log(inputVal)

    fetchData(setBackendData, setHomeKey, inputVal)

    SetInputVal("")
  }

  return (<>
    {/* this is the container for the nav bar */}
    <div className="nav-bar text-center bg-primary">
      <div className="row align-items-center">
        {
          // this code is experimental
          // i'm trying to render returning elements with less lines of code
          // i'm using the map function to map a bunch of names into the same button
          navBarBtns.map((name, index) => {
            return (
              // i'm giving it a key so the data doesn't get lost while procesing
              <div className="col-2" key={index}>
                <button className="btn btn-lg">{name}</button>
              </div>
            )
          })
        }

        <div className="col-4">
          <form className="d-flex" role="search" onSubmit={onSubmit}>
            <input 
              className="form-control me-2" 
              type="search" 
              placeholder="Search" 
              aria-label="Search"
              value={inputVal}
              onChange={(e) => {SetInputVal(e.target.value)}}
            />
            <button className="btn btn-outline-warning" type="submit">Search</button>
          </form>
        </div>
      </div>
    </div>
    
    <div className="row">
      <div className="col-3">
        <div className="container-sm scroll-container m-0 p-3 display-flex">
          {
            // this code is suposed to show the weather of today in a grid
            Object.keys(data.today.timeTable).map(key => {
              return (
                <GridBar 
                  key={key}
                  time={data.today.timeTable[key].time}
                  temp={data.today.timeTable[key].temp}
                  rain={data.today.timeTable[key].rain}
                  img={data.today.timeTable[key].img}
                />
              )
            })
          }
        </div>
      </div>

      <div className="col-9">
        <div className="container">
          <div style={{
            backgroundColor: 'blue',
            border: '2px solid #ccc',
          }}>
            <svg className='p-0 m-0' width="100%" height="100%" viewBox="0 0 370 200" xmlns="http://www.w3.org/2000/svg">
              {/* Rain path */}
              <path className='p-0 m-0' d={data.today.graphString} fill="#4FC3F7" stroke="none" />

              {/* Low Line */}
              <line x1="0" y1="160" x2="370" y2="160" stroke="green" />
              <text x="5" y="155" fill="green" fontSize="7">Low</text>

              {/* Intermediate Line */}
              <line x1="0" y1="100" x2="370" y2="100" stroke="orange" />
              <text x="5" y="95" fill="orange" fontSize="7">Intermediate</text>

              {/* High Line */}
              <line x1="0" y1="40" x2="370" y2="40" stroke="red" />
              <text x="5" y="35" fill="red" fontSize="7">High</text>
            </svg>
          </div>
        </div>

        <div className="row">
          <div className="col-4">
            current time
          </div>

          <div className="col-4 text-center">
            time2
          </div>

          <div className="col-4 text-end">
            time3
          </div>
        </div>
      </div>

    </div>
  </>)
}