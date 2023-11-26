import React, { useState } from 'react'
import Logo from "../Assets/Logo.svg";
import {BsCart2} from "react-icons/bs";
import {HiOutlineBars3} from "react-icons/hi2";
import { Box,Drawer
    ,Home,ListItem
    ,ListItemButton
    ,ListItemicon
    ,ListItemText,
    MpOutlined,
    Phone,
 } from "@mui/icons-material";
 import HomeIcon from "@mui/icons-material/Home"
 import InfoIcon from "@mui/icons-material/Info"
 import CommentRoundedIcon  from '@mui/icons-material/CommentRounded'
 import PhoneRoundedIcon  from '@mui/icons-material/PhoneRounded'
 import ShoppingCartRounded from '@mui/icons-material/ShoppingCartRounded';



const Navbar = () => {

    const [openMenu, setOpenMenu] = useState(false);
    const menuOptions = [
        {
            text:"Home",
            icon:<HomeIcon/>,
        },
        {
            text:"About",
            icon:<InfoIcon/>,
        },
        {
            text:"Testimonials",
            icon:<CommentRoundedIcon/>,
        },
        {
            text:"Contact",
            icon:<PhoneRoundedIcon/>,
        },
        {
            text:"cart",
            icon:<ShoppingCartRounded/>,
        },
    ];
  return  <nav>
    <div className='nav-logo-container'>
        <img src={Logo} alt="" />
    </div>
    <div className='navbar-links-container'>
        <a href="">Home</a>
        <a href="">About</a>
        <a href="">Testimonials</a>
        <a href="">Contact</a>
        <a href="">
            <BsCart2 className='navbar-cart-icon' />
        </a>
        <button className='primary-button'>
            Bookings Now
        </button>
    </div>
    <div className='navbar-menu-container'>
        <HiOutlineBars3 onclick={() => setOpenMenu(true)}/>
    </div>
  </nav>;
};

export default Navbar;
