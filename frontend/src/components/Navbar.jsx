import { NavLink } from 'react-router-dom';

const nav_items = [
    { label: 'Home', path: '/', svg_path: "M575.8 255.5c0 18-15 32.1-32 32.1h-32l.7 160.2c0 2.7-.2 5.4-.5 8.1v16.2c0 22.1-17.9 40-40 40h-16c-1.1 0-2.2 0-3.3-.1-1.4.1-2.8.1-4.2.1L416 512h-24c-22.1 0-40-17.9-40-40v-88c0-17.7-14.3-32-32-32h-64c-17.7 0-32 14.3-32 32v88c0 22.1-17.9 40-40 40h-55.9c-1.5 0-3-.1-4.5-.2-1.2.1-2.4.2-3.6.2h-16c-22.1 0-40-17.9-40-40V360c0-.9 0-1.9.1-2.8v-69.7h-32c-18 0-32-14-32-32.1 0-9 3-17 10-24L266.4 8c7-7 15-8 22-8s15 2 21 7l255.4 224.5c8 7 12 15 11 24z"},
    { label: 'Items', path: '/items', svg_path: "M192 0c-41.8 0-77.4 26.7-90.5 64H64C28.7 64 0 92.7 0 128v320c0 35.3 28.7 64 64 64h256c35.3 0 64-28.7 64-64V128c0-35.3-28.7-64-64-64h-37.5C269.4 26.7 233.8 0 192 0zm0 64a32 32 0 1 1 0 64 32 32 0 1 1 0-64zM72 272a24 24 0 1 1 48 0 24 24 0 1 1-48 0zm104-16h128c8.8 0 16 7.2 16 16s-7.2 16-16 16H176c-8.8 0-16-7.2-16-16s7.2-16 16-16zM72 368a24 24 0 1 1 48 0 24 24 0 1 1-48 0zm88 0c0-8.8 7.2-16 16-16h128c8.8 0 16 7.2 16 16s-7.2 16-16 16H176c-8.8 0-16-7.2-16-16z"},
    { label: 'Orders', path: '/orders', svg_path: "M256 32C192 32 0 64 0 192c0 35.3 28.7 64 64 64v176c0 26.5 21.5 48 48 48h288c26.5 0 48-21.5 48-48V256c35.3 0 64-28.7 64-64C512 64 320 32 256 32z"},
]

function Navbar() {
    return (
        <div className='w-48 p-4 flex flex-col h-screen'>
            <div className='mb-20 text-x1 font-bold text-center'>
                <img src='src/assets/bbb_logo.svg' alt='Bread By Bike Logo' className='h-12 mx-auto' />
            </div>
            <nav className='space-y-2'>
                {nav_items.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `h-20 px-4 py-2 rounded-lg text-sm font-medium mb-10 flex justify-center items-center transition-colors ${
                                isActive
                                    ? 'bg-white text-bbb-blue-500'
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
            </nav>
        </div>
    );
}

export default Navbar