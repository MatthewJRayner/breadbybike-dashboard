function Items() {
    return (
        <div className="flex-col">
            <div className="bg-white shadow-md flex p-4 rounded-2xl text-md">
                <h1 className="text-black_text mr-12">BBB Dashboard <span className="text-gray-300"> | Items</span></h1>
                <div className='flex mr-12'>
                    <h1 className="text-black_text mr-3">Location: </h1>
                    <div className='bg-bbb-blue-500 rounded-2xl pr-3 pl-3 text-bbb-blue-100'>Both</div>
                </div>
                <div className='flex'>
                    <h1 className="text-black_text mr-3">Item </h1>
                    <div className='bg-bbb-blue-500 rounded-2xl pr-3 pl-3 text-bbb-blue-100'>Cinnamon</div>
                </div>
            </div>
        </div>
    );
}

export default Items;