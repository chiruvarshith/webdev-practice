import React, { useState } from 'react';
import QRCodeGenerator from './QrGenerator';
const habitatOptions = [
  'Forest',
  'Savanna',
  'Shrubland',
  'Grassland',
  'Rocky areas',
  'Desert',
];

function AnimalForm() {
  const [formData, setFormData] = useState({
    img_link: '',
    name: '',
    scientific_name: '',
    population_trend: '',
    iucn_status: '',
    wpa: '',
    habitats_and_ecology: '', // This will be a string for selected habitat
    description: '',
    map_img_link: '',
    username: 'sample', // Default username
    password: '123456789',
  });

  const [addedAnimalId, setAddedAnimalId] = useState(null); // State to store the added animal's _id

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('https://zoopark-psi.vercel.app/animals', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log('Animal added successfully:', responseData);
        setAddedAnimalId(responseData._id);
      } else {
        console.error('Failed to add animal:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
         <div className="bg-green-800 text-black h-20 p-2 flex items-center justify-between" style={{ background: "greenyellow", justifyContent: "center", alignItems: "center" }}>
        <div className="flex items-center" style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
          <h2 className="text-xl font-bold">
            ADVANCED INSTITUTE FOR WILDLIFE CONSERVATION
          </h2>

          <p>
            A Government of Tamil Nadu Institute
          </p>
        </div>
      </div>
      {!addedAnimalId && <h1 style={{ textAlign: 'center' }}>Add a New Animal</h1>}
    {!addedAnimalId &&
        <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: '0 auto' }}>
  <label htmlFor="img_link" style={{ display: 'block', margin: '10px 0' }}>Image Link:</label>
  <input
    type="text"
    id="img_link"
    name="img_link"
    value={formData.img_link}
    onChange={handleChange}
    required
    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
  /><br />

  <label htmlFor="name" style={{ display: 'block', margin: '10px 0' }}>Name:</label>
  <input
    type="text"
    id="name"
    name="name"
    value={formData.name}
    onChange={handleChange}
    required
    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
  /><br />

  <label htmlFor="scientific_name" style={{ display: 'block', margin: '10px 0' }}>Scientific Name:</label>
  <input
    type="text"
    id="scientific_name"
    name="scientific_name"
    value={formData.scientific_name}
    onChange={handleChange}
    required
    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
  /><br />

  <label htmlFor="population_trend" style={{ display: 'block', margin: '10px 0' }}>Population Trend:</label>
  <input
    type="text"
    id="population_trend"
    name="population_trend"
    value={formData.population_trend}
    onChange={handleChange}
    required
    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
  /><br />

  <label htmlFor="iucn_status" style={{ display: 'block', margin: '10px 0' }}>IUCN Status:</label>
  <input
    type="text"
    id="iucn_status"
    name="iucn_status"
    value={formData.iucn_status}
    onChange={handleChange}
    required
    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
  /><br />

  <label htmlFor="wpa" style={{ display: 'block', margin: '10px 0' }}>WPA:</label>
  <input
    type="text"
    id="wpa"
    name="wpa"
    value={formData.wpa}
    onChange={handleChange}
    required
    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
  /><br />

  <label htmlFor="habitats_and_ecology" style={{ display: 'block', margin: '10px 0' }}>Habitats and Ecology:</label>
  <select
    id="habitats_and_ecology"
    name="habitats_and_ecology"
    value={formData.habitats_and_ecology}
    onChange={handleChange}
    required
    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
  >
    <option value="">Select Habitat</option>
    {habitatOptions.map((habitat, index) => (
      <option key={index} value={habitat}>
        {habitat}
      </option>
    ))}
  </select><br />

  <label htmlFor="description" style={{ display: 'block', margin: '10px 0' }}>Description:</label>
  <textarea
    id="description"
    name="description"
    value={formData.description}
    onChange={handleChange}
    required
    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
  ></textarea><br />

  <label htmlFor="map_img_link" style={{ display: 'block', margin: '10px 0' }}>Map Image Link:</label>
  <input
    type="text"
    id="map_img_link"
    name="map_img_link"
    value={formData.map_img_link}
    onChange={handleChange}
    required
    style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
  /><br />

  <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Submit</button>
</form>}
{addedAnimalId && (
  <div>
    <h2 style={{ textAlign: 'center' }}>QR Code for the Added Animal:</h2>
    <QRCodeGenerator id={addedAnimalId} />
  </div>
)}

    </div>
  );
}

export default AnimalForm;
