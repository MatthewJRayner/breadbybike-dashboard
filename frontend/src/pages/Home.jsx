import { useState, useEffect } from 'react';

function Home() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/square/stats/');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;
  if (error) return <div className="p-6 text-red-500">Error: {error}</div>;

  return (
    <div className="flex-col">
        <div className="bg-white shadow-md flex p-4 rounded-2xl text-md">
            <h1 className="text-black_text mr-12">BBB Dashboard <span className="text-gray-300"> | Home</span></h1>
            <h1 className="text-black_text mr-3">Location: </h1>
            <div className='bg-bbb-blue-500 rounded-2xl pr-3 pl-3 text-bbb-blue-100'>Both</div>
        </div>
        <div className="p-6">
            <h1 className="text-2xl font-bold">Home Dashboard</h1>
            <p>Welcome to the Bread by Bike Dashboard!</p>
            {stats && (
                <div className="mt-4 p-4 bg-gray-100 rounded-lg">
                    <h2 className="text-lg font-semibold">Sales Stats</h2>
                    <p>Total Sales: ${stats.total_sales}</p>
                    <p>Order Count: {stats.order_count}</p>
                    <p>Average Order Value: ${stats.average_order_value}</p>
                </div>
            )}
        </div>
    </div>
    
  );
}

export default Home;