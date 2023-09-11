import Navbar from './components/navbar/navbar'
import image from './assets/royal-bengal02.png';
import background from './assets/leaf-background.webp';
import './index.css'
import Tiger from "./components/tiger";
import Elephant from './components/elephant';
import Leopard from './components/leopard';
import Admin from './components/admin';
import React, { Component } from 'react';
import AnimalDetailsPage from './components/AnimalDetailsPage';
import QRCodeGenerator from './components/QrGenerator';
import { BrowserRouter as Router,Routes, Route, Link } from 'react-router-dom';
import AnimalForm from './components/home';
<meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
function App() {
  return (
    <Router>
<div className="webpage" >
       <Routes>
                {/* <Route exact path='tiger' element={< Tiger />}></Route>
                <Route exact path='/elephant' element={< Elephant />}></Route>
                <Route exact path='/leopard' element={< Leopard />}></Route> */}
                <Route exact path='/form' element={< AnimalForm/>}></Route>
                <Route exact path='/qr-generator' element={<QRCodeGenerator/>}></Route>
                <Route exact path='/:id' element={< AnimalDetailsPage/>}></Route>
                <Route exact path='/admin' element={< Admin/>}></Route>
        </Routes>
      </div>
    </Router>
    
      

    
  );
}

export default App;
