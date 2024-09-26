import React, { useEffect, useState } from 'react';
import { MdOutlineAccountCircle } from "react-icons/md";
import {useNavigate} from 'react-router-dom';


import background from '/Users/akashbalaji/Desktop/Fruit_SpoilDetection/frontend/src/assets/BG_random2.png';

function Dashboard() {
  const [items, setItems] = useState([]);
  const navigate = useNavigate();


  useEffect(() => {
    // Fetch data from API
    const fetchData = async () => {
      try {
        // Replace with your API URL
        const response = await fetch('https://hchjn6x7-8000.inc1.devtunnels.ms/get_data');
        
        // Check if response is ok
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        // Extract data
        const responseData = await response.json();
        
        // Assuming responseData is in the format mentioned
        const jsonString = responseData[0]; // Extracting the string from array
        const data = JSON.parse(jsonString); // Parsing JSON string into an object

        setItems(data); // Setting state with parsed data
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []); // Empty dependency array means this effect runs once when the component mounts

  return (
    <div className="min-h-screen flex">
    {/* Left Sidebar */}
    <div className="bg-maroon w-64 p-3 text-black flex flex-col justify-between" style={{backgroundColor: "#f4f1de"}}>
        <div>
            <h1 className="text-3xl font-bold">Frutech</h1>
        </div>

        {/* Icon Container */}
        <div className="flex justify-left pb-1" onClick={()=> navigate("/")}>
            <MdOutlineAccountCircle style={{ fontSize: 33 }} />
            <h2 className="text-2xl font-light ml-2">Admin</h2>
        </div>
    </div>

    {/* Main Content */}
    <div className="flex-grow bg-cover bg-center relative" style={{ backgroundImage: `url(${background})`, backgroundColor: 'rgba(0, 0, 0, 0.2)', /* Dark overlay color */
        backgroundBlendMode: 'overlay' }}>
        <div className="bg-white bg-opacity-60 rounded-md mt-10 mx-10 p-6 shadow-lg">
        <div className="flex flex-col space-y-4">
        <h2 className="text-2xl font-semibold ml-2">Inventory</h2>
            {/* Title Row */}
            <div className="flex p-4 rounded-md shadow-md" style={{backgroundColor: "#f4f1de"}}>
            <div className="flex-1 font-bold">S.no</div>
            <div className="flex-1 font-bold">Item</div>
            <div className="flex-1 font-bold">Production Date</div>
            <div className="flex-1 font-bold">Expiry Date</div>
            </div>

            {/* Data Rows */}
            {items.map((item, index) => (
            <div key={index} className="flex bg-gray-200 p-4 rounded-md shadow-md" style={{backgroundColor: "#FFFEF5"}}>
                <div className="flex-1">{index + 1}</div>
                <div className="flex-1">{item.item_name}</div>
                <div className="flex-1">{item.Product_date}</div>
                <div className="flex-1">{item.Expiry_date}</div>
            </div>
            ))}

        </div>
        </div>
    </div>
    </div>
  );
}

export default Dashboard;
