import React, { useEffect, useState } from 'react';
import { MdOutlineAccountCircle } from "react-icons/md";
import { useNavigate } from 'react-router-dom';

import background from '/Users/akashbalaji/Desktop/Fruit_SpoilDetection/frontend/src/assets/BG_random2.png';

function Dashboard() {
  const [items, setItems] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Function to fetch data
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/get_data');

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setItems(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Fetch data initially when component mounts
    fetchData();

    const intervalId = setInterval(fetchData, 30000);

    // Clean up the interval when component unmounts
    return () => clearInterval(intervalId);
  }, []);

  // Function to calculate the number of days left
  const calculateDaysLeft = (prodDate, expiryDate) => {
    if (!expiryDate || expiryDate === "NULL" || expiryDate === "") {
      return "-"; // Return "-" if expiryDate is NULL or empty
    }
  
    const productionDate = new Date(prodDate);
    const expiryDateObj = new Date(expiryDate);
    const currentDate = new Date();
  
    // Subtract the time already passed
    const elapsedTime = Math.floor((currentDate - productionDate) / (1000 * 60 * 60 * 24));
    
    // Calculate the total days left
    const totalDaysLeft = Math.floor((expiryDateObj - currentDate) / (1000 * 60 * 60 * 24));
    
    // Adjust the predicted days left by subtracting the days already passed
    const daysLeft = totalDaysLeft - elapsedTime;
  
    return daysLeft < 1 ? "Expired" : `${daysLeft} days left`;
  };
  

  return (
    <div className="min-h-screen flex">
      {/* Left Sidebar */}
      <div className="bg-maroon w-64 text-black flex flex-col justify-between" style={{ backgroundColor: "#f4f1de" }}>
        <div>
          <h1 className="text-3xl p-3 font-bold">Frutech</h1>

          <div className='flex-col mt-5 gap-3'>
            <div className='hover:bg-[#d1ceba] bg-[#d1ceba]' onClick={() => navigate("/dashboard")}>
              <h3 className="text-2xl p-3 font-medium">Inventory</h3>
            </div>

            <div className='hover:bg-[#d1ceba]' onClick={() => navigate("/storage")}>
              <h3 className="text-2xl p-3 font-medium">Storage</h3>
            </div>
          </div>
        </div>

        {/* Icon Container */}
        <div className="flex justify-left pb-1 p-3" onClick={() => navigate("/")}>
          <MdOutlineAccountCircle style={{ fontSize: 33 }} />
          <h2 className="text-2xl font-light ml-2">Admin</h2>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-grow bg-cover bg-center relative" style={{ backgroundImage: `url(${background})`, backgroundColor: 'rgba(0, 0, 0, 0.2)', /* Dark overlay color */
        backgroundBlendMode: 'overlay' }}>
        <div className="bg-white bg-opacity-60 rounded-md mt-20 mx-10 p-6 shadow-lg" style={{ display: 'flex', flexDirection: 'column', height: '80vh' }}>
          {/* Title Section */}
          <div className="flex flex-col space-y-4">
            <h2 className="text-2xl font-semibold ml-2">Inventory</h2>
          </div>

          {/* Title Row - Fixed and not scrollable */}
          <div className="flex p-4 mt-2 rounded-md shadow-md" style={{ backgroundColor: "#f4f1de" }}>
            <div className="flex-1 font-bold">S.no</div>
            <div className="flex-1 font-bold">Item</div>
            <div className="flex-1 font-bold">Production Date</div>
            <div className="flex-1 font-bold">Days Left</div>
          </div>

          {/* Scrollable Data Rows */}
          <div className='mt-5' style={{ flexGrow: 1, overflowY: 'auto' }}>
            {/* Data Rows with Gap */}
            {items.map((item, index) => (
              <div key={index} className="flex bg-gray-200 p-4 mb-4 rounded-md shadow-md" style={{ backgroundColor: "#FFFEF5" }}>
                <div className="flex-1">{index + 1}</div>
                <div className="flex-1">{item.item_name}</div>
                <div className="flex-1">{item.Product_date}</div>
                <div className="flex-1" style={{ color: calculateDaysLeft(item.Product_date, item.Expiry_date) === "Expired" ? 'red' : 'black' }}>
                  {calculateDaysLeft(item.Product_date, item.Expiry_date)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
