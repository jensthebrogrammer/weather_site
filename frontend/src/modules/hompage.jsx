import React from "react";
import { Link } from "react-router-dom";
import GridBar from "./gridBar";
import { useState } from "react";
import { fetchData } from "../scripts/usingData";
import "/Users/35257/PycharmProjects/weather_app/frontend/src/App.css"


export default function Homepage({data, setBackendData, setHomeKey}) {
  // this code is expirimental. i'm generating html using js
  const navBarBtns = ["btn1", 'btn2']
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
              <div className="col-3" key={index}>
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
    
    <div className="container-sm scroll-container m-0 p-3">
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
  </>)
}