import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { Routes, Route } from "react-router-dom";
import logo from './logo.svg';
import './App.css';

import GeneralUser from "./components/GeneralUser";
import Admin from "./components/Admin";
import Navbar from "./components/Navbar";
import PhotoPortal from "./components/PhotoPortal";


function App() {

  return (
    <Routes>
      {/* path defines the URL, element defines what component to render */}
      <Route path="/" element={<GeneralUser />} />
      <Route path="/admin" element={<Admin />} /> 
      <Route path="/photo-portal" element={
	      <>
	      <Navbar />
	      <PhotoPortal />
	      </>
      } 
      />
    </Routes>
  );
}

export default App;

