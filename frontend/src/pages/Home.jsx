function Home() {
    return (
        <div className="flex-col">
            <div className="bg-white shadow-md flex p-4 rounded-2xl text-md">
                <h1 className="text-black_text mr-12">BBB Dashboard <span className="text-gray-300"> | Home</span></h1>
                <h1 className="text-black_text mr-3">Location: </h1>
                <div className='bg-bbb-blue-500 rounded-2xl pr-3 pl-3 text-bbb-blue-100'>Both</div>
            </div>
        </div>
    );
}

export default Home;