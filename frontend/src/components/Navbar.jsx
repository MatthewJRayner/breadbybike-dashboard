import { NavLink, useNavigate } from 'react-router-dom';
import React, { useState } from 'react';

const Navbar = () => {
    const [menuOpen, setMenuOpen] = useState(false);
    const navigate = useNavigate();

    const nav_items = [
        { label: 'Home', path: '/', svg_path: "M575.8 255.5c0 18-15 32.1-32 32.1h-32l.7 160.2c0 2.7-.2 5.4-.5 8.1v16.2c0 22.1-17.9 40-40 40h-16c-1.1 0-2.2 0-3.3-.1-1.4.1-2.8.1-4.2.1L416 512h-24c-22.1 0-40-17.9-40-40v-88c0-17.7-14.3-32-32-32h-64c-17.7 0-32 14.3-32 32v88c0 22.1-17.9 40-40 40h-55.9c-1.5 0-3-.1-4.5-.2-1.2.1-2.4.2-3.6.2h-16c-22.1 0-40-17.9-40-40V360c0-.9 0-1.9.1-2.8v-69.7h-32c-18 0-32-14-32-32.1 0-9 3-17 10-24L266.4 8c7-7 15-8 22-8s15 2 21 7l255.4 224.5c8 7 12 15 11 24z"},
        { label: 'Items', path: '/items', svg_path: "M256 32C192 32 0 64 0 192c0 35.3 28.7 64 64 64v176c0 26.5 21.5 48 48 48h288c26.5 0 48-21.5 48-48V256c35.3 0 64-28.7 64-64C512 64 320 32 256 32z"},
        { label: 'Orders', path: '/orders', svg_path: "M192 0c-41.8 0-77.4 26.7-90.5 64H64C28.7 64 0 92.7 0 128v320c0 35.3 28.7 64 64 64h256c35.3 0 64-28.7 64-64V128c0-35.3-28.7-64-64-64h-37.5C269.4 26.7 233.8 0 192 0zm0 64a32 32 0 1 1 0 64 32 32 0 1 1 0-64zM72 272a24 24 0 1 1 48 0 24 24 0 1 1-48 0zm104-16h128c8.8 0 16 7.2 16 16s-7.2 16-16 16H176c-8.8 0-16-7.2-16-16s7.2-16 16-16zM72 368a24 24 0 1 1 48 0 24 24 0 1 1-48 0zm88 0c0-8.8 7.2-16 16-16h128c8.8 0 16 7.2 16 16s-7.2 16-16 16H176c-8.8 0-16-7.2-16-16z"},
    ];

    const handleLogout = () => {
        localStorage.removeItem('accessLevel');
        localStorage.removeItem('lastStatsUpdatetime');
        localStorage.removeItem('sessionStart');
        navigate('/login');
    };

    return (
        <div className='w-full lg:w-48 lg:h-screen p-4 flex-col'>
            {/* Logo and Hamburger */}
            <div className='flex items-center justify-between lg:justify-center lg:mb-16 lg:mt-3'>
                <img src='src/assets/bbb_logo.svg' alt='Bread By Bike Logo' className='h-5 lg:h-10' />
                <button className='lg:hidden focus:outline-none' onClick={() => setMenuOpen(!menuOpen)} aria-label='Toggle Menu'>
                    <svg class='fill-bbb-blue-500 size-5' viewBox='0 0 640 640'>
                        <path d='M96 160c0-17.7 14.3-32 32-32h384c17.7 0 32 14.3 32 32s-14.3 32-32 32H128c-17.7 0-32-14.3-32-32zm0 160c0-17.7 14.3-32 32-32h384c17.7 0 32 14.3 32 32s-14.3 32-32 32H128c-17.7 0-32-14.3-32-32zm448 160c0 17.7-14.3 32-32 32H128c-17.7 0-32-14.3-32-32s14.3-32 32-32h384c17.7 0 32 14.3 32 32z' />
                    </svg>
                </button>
            </div>

            {/* Navigation Links */}
            <nav className={`${menuOpen ? 'block' : 'hidden'} lg:block mt-10 lg:mt-0`}>
                <div className='space-y-2'>
                    {nav_items.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            onClick={() => setMenuOpen(false)}
                            className={({ isActive }) =>
                                `h-12 px-4 py-2 rounded-lg text-sm font-medium mb-15 flex justify-center items-center transition-colors ${
                                    isActive
                                        ? 'bg-white text-bbb-blue-500 shadow-md'
                                        : 'text-text_black hover:bg-bbb-blue-100'
                                }`
                            }
                        >
                            <svg viewBox='0 0 576 512' class='size-5 fill-current'>
                                <path d={item.svg_path} />
                            </svg>
                            <span className='ml-3'>{item.label}</span>
                        </NavLink>
                    ))}
                    <div onClick={handleLogout} className='flex justify-center items-center px-4 py-2 h-12 rounded-lg text-sm font-medium mb-15 transition-colors shadow-md bg-bbb-blue-500 hover:bg-bbb-blue-400 hover:cursor-pointer'>
                        <svg class='fill-white size-5' viewBox='0 0 640 640'>
                            <path d='M569 337c9.4-9.4 9.4-24.6 0-33.9L425 159c-6.9-6.9-17.2-8.9-26.2-5.2S384 166.3 384 176v80H272c-26.5 0-48 21.5-48 48v32c0 26.5 21.5 48 48 48h112v80c0 9.7 5.8 18.5 14.8 22.2 9 3.7 19.3 1.7 26.2-5.2l144-144zM224 160c17.7 0 32-14.3 32-32s-14.3-32-32-32h-64c-53 0-96 43-96 96v256c0 53 43 96 96 96h64c17.7 0 32-14.3 32-32s-14.3-32-32-32h-64c-17.7 0-32-14.3-32-32V192c0-17.7 14.3-32 32-32h64z' />
                        </svg>
                        <span className='text-white ml-3'>Logout</span>
                    </div>
                </div>
            </nav>
        </div>
    );
}

export default Navbar