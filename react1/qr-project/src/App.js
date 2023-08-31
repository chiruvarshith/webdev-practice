import React from "react";
import Navbar from './components/navbar/navbar'
import image from './assets/royal-bengal02.png';
import background from './assets/leaf-background.webp';
import './index.css'
<meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
 
function App() {
  return (
    <div className="webpage" >
      
      <div className="heading">
        <h1>Bengal Tiger</h1>
      </div>
      <div className="image">
        <img src={image} className="tiger-image"  />
      </div>
      <div className="paragraph1">
      The Bengal tiger is the national animal of India and holds 
      significant cultural and religious importance in the region. It appears in various Indian myths and legends.
      </div>
     </div> 
      

    
  );
}

export default App;
