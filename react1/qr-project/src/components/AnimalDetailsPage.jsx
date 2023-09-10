import React, { useEffect, useState } from 'react';
import { useParams } from "react-router-dom";
import decrease from '../assets/icons/decrease.png'
import increase from '../assets/icons/increase.png'

function AnimalDetailsPage(){
    let { id } = useParams();
    const [animalData, setAnimalData] = useState(null);
  
    useEffect(() => {
      // Construct the URL with the id parameter
      const apiUrl = `https://zoopark-psi.vercel.app/animals/${id}`;
  
      // Fetch data from the API
      fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => {
          setAnimalData(data);
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
    }, [id]);
  
    return  (
      <div className='m-5 '>
          <div class="relative rounded-xl">
              <img class="h-auto max-w-full rounded-xl" src={animalData.img_link} alt="image description" />
              <div class="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-black to-transparent flex items-center justify-center rounded-xl">
                  <h2 class="text-white font-semibold">{animalData.name}</h2>
              </div>
          </div>
          <p className='m-0 p-0'>Scientific name</p>
          <h1 className='m-0'>{animalData.scientific_name}</h1>
          <div className="flex justify-content-center align-items-center space-between">
          <div className="flex-1">
            {animalData.population_trend === "decrease" ? (
              <div className="bg-red-300 bg-opacity-30 rounded-lg p-2 inline-block">
                <img className="w-5" src={decrease} alt="Decrease Icon" />
              </div>
            ) : (
              <div className="bg-green bg-opacity-30 rounded-lg p-2 inline-block">
                <img className="w-5" src={increase} alt="Increase Icon" />
              </div>
            )}
            <p>Population trend</p>
          </div>

              <div class="flex-1 flex flex-col justify-end">
                  <h4 className='bg-red-300 bg-opacity-30 rounded-lg p-2 self-center'> {animalData.iucn_status}</h4>
                  <p class="self-center">IUCN status</p>
              </div>
    
              <div class="flex-1 flex flex-col justify-end">
                  <p class="self-center font-semibold">{animalData.wpa}</p>
                  <p class="self-center ">WPA</p>
              </div>
          </div>
          <h2 className="self-center font-semibold mt-5">HABITAT AND ECOLOGY</h2>
          <div className="flex flex-wrap">
            {animalData?.habitats_and_ecology.map((habitat, index) => (
              <div
                key={index}
                className={`bg-green-500 text-white px-3 py-1 m-2 rounded-full`}
              >
                {habitat}
              </div>
            ))}
          </div>
    
          <h2 className="self-center font-semibold mt-5">Description</h2>
          <p>{animalData?.description}</p>
          <img
            className="h-auto max-w-full rounded-xl"
            src={animalData?.map_img_link}
            alt={`${animalData?.name} Map`}
          />
        </div>
    )
}
export default AnimalDetailsPage;

