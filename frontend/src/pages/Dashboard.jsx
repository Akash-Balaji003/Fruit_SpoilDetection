import React, { useEffect, useState } from 'react';
import { MdOutlineAccountCircle } from "react-icons/md";
import { useNavigate } from 'react-router-dom';
import { FaArrowUp, FaArrowDown } from 'react-icons/fa'; // Import icons for arrows

import background from '/Users/akashbalaji/Desktop/Fruit_SpoilDetection/frontend/src/assets/BG_random2.png';

function Dashboard() {
    const [items, setItems] = useState([]);
    const [prevDaysLeft, setPrevDaysLeft] = useState({}); // State to track previous days left for each item
    const [manureResults, setManureResults] = useState({}); // Initialize manureResults state here
    const [expandedRow, setExpandedRow] = useState(null); // Expanded row state
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

            // Calculate days left for each item and compare with the previous state
            const updatedItems = data.map(item => {
            const currentDaysLeft = calculateDaysLeft(item.Product_date, item.Expiry_date);
            const previousDays = prevDaysLeft[item.item_name] || currentDaysLeft;
            
            const daysIncreased = currentDaysLeft > previousDays;
            const daysDecreased = currentDaysLeft < previousDays;
            
            return {
                ...item,
                currentDaysLeft,
                daysIncreased,
                daysDecreased
            };
            });
            
            setItems(updatedItems);
            
            // Update the previous days left with the current data
            setPrevDaysLeft(prev => {
            const newPrevDaysLeft = updatedItems.reduce((acc, item) => {
                acc[item.item_name] = item.currentDaysLeft;
                return acc;
            }, {});

            return newPrevDaysLeft;
            });
        } catch (error) {
            console.error('Error fetching data:', error);
        }
        };

        // Fetch data initially when component mounts
        fetchData();

        const intervalId = setInterval(fetchData, 30000); // Call every 30 seconds

        // Clean up the interval when component unmounts
        return () => clearInterval(intervalId);
    }, []); // Only run once on component mount, no dependencies

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
    
        return daysLeft < 1 ? "Expired" : daysLeft;
    };

    const handleCheck = async (item) => {
        // Ensure that weight is defined and a valid number
        if (!item.Quantity || isNaN(item.Quantity)) {
        console.error('Invalid weight:', item.Quantity);
        return;
        }
    
        const payload = {
        fruit_name: item.item_name,  // Should be a string
        weight: parseFloat(item.Quantity)  // Ensure this is a number
        };
    
        try {
        const response = await fetch('http://127.0.0.1:8000/poster', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)  // Send the payload
        });
    
        if (!response.ok) {
            throw new Error('Error fetching manure prediction');
        }
    
        const prediction = await response.json();
    
        setManureResults(prev => ({
            ...prev,
            [item.item_name]: prediction
        }));
    
        setExpandedRow(expandedRow === item.item_name ? null : item.item_name); // Toggle the expanded row
        } catch (error) {
        console.error('Error fetching prediction:', error);
        }
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
        <div className="flex-grow bg-cover bg-center relative" style={{ backgroundImage: `url(${background})`, backgroundColor: 'rgba(0, 0, 0, 0.2)', backgroundBlendMode: 'overlay' }}>
            <div className="bg-white bg-opacity-60 rounded-md mt-20 mx-10 p-6 shadow-lg" style={{ display: 'flex', flexDirection: 'column', maxHeight: '80vh' }}>
            {/* Title Section */}
            <div className="flex flex-col space-y-4">
                <h2 className="text-2xl font-semibold ml-2">Inventory</h2>
            </div>

            {/* Title Row */}
            <div className="flex p-4 mt-2 rounded-md shadow-md" style={{ backgroundColor: "#f4f1de" }}>
                <div className="flex-1 font-bold">S.no</div>
                <div className="flex-1 font-bold">Item</div>
                <div className="flex-1 font-bold">Production Date</div>
                <div className="flex-1 font-bold">Days Left</div>
            </div>

            {/* Scrollable Data Rows */}
            <div className='mt-5' style={{ flexGrow: 1, maxHeight: 'calc(80vh - 100px)', overflowY: 'auto' }}>
                {items.length === 0 ? (
                <div className="text-center text-gray-500 mt-10">The storage is empty</div>
                ) : (
                items.map((item, index) => (
                    <div key={index} className="flex flex-col bg-gray-200 p-4 mb-4 rounded-md shadow-md" style={{ backgroundColor: "#FFFEF5" }}>
                    <div className="flex">
                        <div className="flex-1">{index + 1}</div>
                        <div className="flex-1">{item.item_name}</div>
                        <div className="flex-1">{item.Product_date}</div>
                        <div className="flex-1 flex items-center justify-between" style={{ color: item.currentDaysLeft === "Expired" ? 'red' : 'black' }}>
                        <div className='flex gap-1'>
                            {item.daysIncreased && <FaArrowUp style={{ color: 'green', marginLeft: 5, fontSize: '1em', marginTop: 4 }} />}
                            {item.daysDecreased && <FaArrowDown style={{ color: 'red', marginLeft: 5, fontSize: '1em', marginTop: 4 }} />}
                            {item.currentDaysLeft === "Expired" ? "Expired" : `${item.currentDaysLeft} days left`}
                        </div>

                        {item.currentDaysLeft === "Expired" && (
                            <button
                            type="submit"
                            className="bg-blue-800 text-white py-1 px-2 rounded hover:bg-blue-700"
                            onClick={() => handleCheck(item)}
                            >
                            Check
                            </button>
                        )}
                        </div>
                    </div>

                    {/* Expanded Row */}
                    {expandedRow === item.item_name && (
                        <div className="mt-2 bg-gray-100 p-4 rounded-md">
                        {manureResults[item.item_name] ? (
                            manureResults[item.item_name].map((result, index) => (
                            <div key={index} className="mb-2 flex-row justify-between">
                                <p><strong>Method:</strong> {result.Method}</p>
                                <p><strong>Time to Manure:</strong> {result.Time_to_Manure} weeks</p>
                                <p><strong>Predicted Manure Weight:</strong> {result.Predicted_Manure_Weight.toFixed(2)} kg</p>
                            </div>
                            ))
                        ) : (
                            <p>Loading prediction...</p>
                        )}
                        </div>
                    )}
                    </div>
                ))
                )}
            </div>
            </div>
        </div>
        </div>
    );
}

export default Dashboard;
