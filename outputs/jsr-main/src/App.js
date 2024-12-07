import "./App.css";
import React, { useState } from "react";
import Papa from "papaparse";
import Navbar from "./Components/Navbar";
import { Route, Routes } from "react-router-dom";
import Home from "./Components/Home";
import Login from "./Components/Login";
import Signup from "./Components/Signup";
import Dashboard from "./Components/Dashboard";
import ImageUploadForm from "./Components/ImageUploadForm";

import Segmented from "./Components/Segmented";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div className="w-screen h-screen bg-richblack-900 flex flex-col ">
      <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />

      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route
          path="/login"
          element={<Login setIsLoggedIn={setIsLoggedIn} />}
        ></Route>
        <Route
          path="/signup"
          element={<Signup setIsLoggedIn={setIsLoggedIn} />}
        ></Route>
        <Route path="/dashboard" element={<Dashboard />}></Route>
        <Route path="model" element={<ImageUploadForm />}></Route>

        <Route path="/" element={<ImageUploadForm />} />
      </Routes>
    </div>
  );
}

export default App;
