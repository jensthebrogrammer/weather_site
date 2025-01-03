import React from "react";
import { Link } from "react-router-dom";


export default function Homepage() {
  return (<>
    <Link to="/testing_page">
      <button className="btn btn-lg btn-outline-primary">test</button>
    </Link>
  </>)
}