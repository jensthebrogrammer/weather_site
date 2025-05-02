import React from "react";
import { Link } from "react-router-dom";
import GridBar from "./gridBar";
import "/Users/35257/PycharmProjects/weather_app/frontend/src/App.css"


export default function Homepage({data}) {
  // this code is expirimental. i'm generating html using js
  const navBarBtns = ["btn1", 'btn2', 'btn3', 'btn4']

  console.log(data)

  return (<>
    {/* this is the container for the nav bar */}
    <div className="nav-bar text-center bg-primary">
      <div className="row">
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
      </div>
    </div>
    
    <div className="container m-0 p-3">
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