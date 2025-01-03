import React from "react";
import { Link } from "react-router-dom";


export default function Homepage() {
  // this code is expirimental. i'm generating html using js
  const navBarBtns = ["btn1", 'btn2', 'btn3', 'btn4']

  return (<>
    {/* this is the container for the nav bar */}
    <div className="nav-bar text-center bg-primary">
      <div className="row">
        {
          // this code is experimental
          // i'm trying to render returning elements with less lines of code
          // i'm using the map function to map a bunch of names into the same button
          navBarBtns.map((name) => {
            return (
              <div className="col-3">
                <button className="btn btn-lg">{name}</button>
              </div>
            )
          })
        }
      </div>
    </div>
  </>)
}