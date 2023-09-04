//Leopard
import React from 'react';
import image from '../assets/images/leopard.png'
import decrease from '../assets/icons/decrease.png'
import map from '../assets/images/leopard_map.png'
function Leopard (){
    return (
        <div className='m-5 '>
            <div class="relative rounded-xl">
                <img class="h-auto max-w-full rounded-xl" src={image} alt="image description" />
                <div class="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-black to-transparent flex items-center justify-center rounded-xl">
                    <h2 class="text-white font-semibold">Indian Leopard</h2>
                </div>
            </div>
            <p className='m-0 p-0'>Scientific name</p>
            <h1 className='m-0'>Panthera pardus fusca</h1>
            <div class="flex justify-content-center align-items-center space-between">
                <div class="flex-1 ">
                    <div class="bg-red-300 bg-opacity-30 rounded-lg p-2 inline-block">
                        <img class="w-5" src={decrease} alt="Decrease Icon" />
                    </div>


                    <p>Population trend</p>
                </div>
                <div class="flex-1 flex flex-col justify-end">
                    <h4 className='bg-red-300 bg-opacity-30 rounded-lg p-2 self-center'>Vulnerable</h4>
                    <p class="self-center">IUCN status</p>
                </div>

                <div class="flex-1 flex flex-col justify-end">
                    <p class="self-center font-semibold">schedule 1</p>
                    <p class="self-center ">WPA</p>
                </div>
            </div>
            <h2 class="self-center font-semibold mt-5">HABITAT AND ECOLOGY</h2>
            <div class="flex flex-wrap">
                <div class="bg-green-500 text-white px-3 py-1 m-2 rounded-full">Forest</div>
                <div class="bg-yellow-500 text-white px-3 py-1 m-2 rounded-full">Savanna</div>
                <div class="bg-yellow-400 text-white px-3 py-1 m-2 rounded-full">Shrubland</div>
                <div class="bg-blue-500 text-white px-3 py-1 m-2 rounded-full">Grassland</div>
                <div class="bg-gray-500 text-white px-3 py-1 m-2 rounded-full">Rocky areas</div>
                <div class="bg-orange-500 text-white px-3 py-1 m-2 rounded-full">Desert</div>
            </div>

            <h2 class="self-center font-semibold mt-5">Description</h2>
            <p>
            The Indian leopard (Panthera pardus fusca) is a subspecies of leopard native to the Indian subcontinent </p>
            <img class="h-auto max-w-full rounded-xl" src={map} alt="image description" />
        </div>
    )
}
export default Leopard;
