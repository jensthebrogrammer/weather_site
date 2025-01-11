import React from "react";
import { Link } from "react-router-dom";


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
  </>)
}