import React from 'react';
import './tiger.css'; // Create a CSS file for styling
import tiger_image from "../assets/royal-bengal02.png"
import tiger_map from "../assets/tiget_map.png"
function Tiger() {
  return (
    <div className="tiger-card">
      <h1>Tiger</h1>
      <img src={tiger_image} className='tiget-image'/>
      <div className="info">
        <h2>Common Name</h2>
        <p>Bengal Tiger</p>

        <h2>Scientific Name</h2>
        <p>Panthera tigris tigris</p>

        <h2>Description</h2>
        <p>
          The Bengal tiger is a population of the Panthera tigris tigris
          subspecies and the nominate tiger subspecies. It ranks among the
          biggest wild cats alive today. It is considered to belong to the
          world's charismatic megafauna.
        </p>

        <h2>Graphical Distribution</h2>
      <img src={tiger_map} className='tiget-image'/>

        {/* Add graphical distribution information here, you can use images or maps if available. */}

        <h2>Population Trend</h2>
        <p>Decreasing</p>

        <h2>Habitat and Ecology</h2>
        <ul>
          <li>Forest</li>
          <li>Savanna</li>
          <li>Shrubland</li>
          <li>Grassland</li>
          <li>Wetlands (inland)</li>
          <li>Marine Coastal/Supratidal</li>
          <li>Artificial/Terrestrial</li>
        </ul>

        <h2>IUCN Status</h2>
        <p>Endangered</p>

        <h2>WPA Schedule</h2>
        {/* Add WPA schedule information here if applicable. */}
      </div>
    </div>
  );
}

export default Tiger;
