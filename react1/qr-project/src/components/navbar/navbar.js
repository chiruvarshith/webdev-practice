import React from 'react'
import {BiSearch} from 'react-icons/bi'
import {BsPerson} from 'react-icons/bs'
import {HiOutlineMenuAlt4} from 'react-icons/hi'

import './navbarstyles.css'

function navbar() {
  return (
    
    <div className='navbar'>
        <div className='logo'>
            <h2>ZOO</h2>
        </div>
        <ul className='nav-menu'>
        <li>Home</li>
        <li>About</li>
        <li>FAQ</li>
        <li>Contact us</li>
        </ul>
        <div className='nav-icons'>
            <BiSearch className='icon' />
            <BsPerson className='icon' />
        </div>
        <div className='hamburger'>
            <HiOutlineMenuAlt4 className='icon' />
        </div>

        <div className='mobile-menu'>
            <ul className='mobile-nav'>
            <li>Home</li>
            <li>About</li>
            <li>FAQ</li>
            <li>Contact us</li>
            </ul>
            <div className='mobile-menu-bottom'>
                <div className='menu-icons'>
                    <button></button>
                </div>
                <div className='social-icons'></div>
            </div>
        </div>
    </div>
    
  )
}

export default navbar