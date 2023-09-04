//
import React from 'react';
import ima from "../assets/images/elephant.png"
function Elephant (){
    return (
        <div className='m-5 '>
            <div class="relative">
                <img class="h-auto max-w-full rounded-xl" src={ima} alt="image description"/>
                <div class="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-black to-transparent flex items-center justify-center">
                    <h2 class="text-white font-semibold">elephant</h2>
                </div>
            </div>
        </div>


        

    )
}
  
export default Elephant;