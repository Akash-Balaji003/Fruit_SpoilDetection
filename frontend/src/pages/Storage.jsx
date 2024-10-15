import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { IoMdClose } from "react-icons/io";
import { MdOutlineAccountCircle } from "react-icons/md";
import background from '/Users/akashbalaji/Desktop/Fruit_SpoilDetection/frontend/src/assets/BG_random2.png';

function Storage() {
    const [items, setItems] = useState([]);
    const [newItem, setNewItem] = useState({ name: '', quantity: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleAddItem = () => {
        if (newItem.name && newItem.quantity) {
            setItems([...items, { ...newItem, quantity: parseFloat(newItem.quantity) }]); // Parse quantity to float
            setNewItem({ name: '', quantity: '' });
            setError(''); // Clear the error message on successful addition
        } else {
            setError('Please fill in both item name and quantity');
        }
    };    

    const handleRemoveItem = (index) => {
        const updatedItems = items.filter((_, i) => i !== index);
        setItems(updatedItems);
    };

    const handleSubmit = async () => {
        if (items.length === 0) {
            setError('No items to submit. Please add at least one item.');
        } else {
            setError('');
            try {
                // Log the data being sent
                console.log('Submitting items:', items);
                
                const response = await fetch('http://127.0.0.1:8000/initial_storage', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(items),
                });
    
                // Check for response status and log it
                console.log('Response status:', response.status);
    
                if (!response.ok) {
                    const errorData = await response.json();
                    console.log('Error details:', errorData); // Log server error details
                    throw new Error('Failed to submit items');
                }
    
                const result = await response.json();
                console.log('Items submitted:', result.message);
            } catch (error) {
                console.error('Error submitting items:', error);
            }
        }
    };
    
    

    return (
        <div className="min-h-screen flex">
            {/* Left Sidebar */}
            <div className="bg-maroon w-64 text-black flex flex-col justify-between" style={{ backgroundColor: "#f4f1de" }}>
                <div>
                    <h1 className="text-3xl p-3 font-bold">Frutech</h1>

                    <div className='flex-col mt-5 gap-3'>
                        <div className='hover:bg-[#d1ceba]' onClick={() => navigate("/dashboard")}>
                            <h3 className="text-2xl p-3 font-medium">Inventory</h3>
                        </div>

                        <div className='hover:bg-[#d1ceba] bg-[#d1ceba]' onClick={() => navigate("/storage")}>
                            <h3 className="text-2xl p-3 font-medium">Storage</h3>
                        </div>
                    </div>
                </div>

                {/* Icon Container */}
                <div className="flex justify-left pb-1" onClick={() => navigate("/")}>
                    <MdOutlineAccountCircle style={{ fontSize: 33 }} />
                    <h2 className="text-2xl font-light ml-2">Admin</h2>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-grow bg-cover bg-center relative" style={{
                backgroundImage: `url(${background})`,
                backgroundColor: 'rgba(0, 0, 0, 0.2)',
                backgroundBlendMode: 'overlay'
            }}>
                <div className="bg-white bg-opacity-60 rounded-md mt-20 mx-10 p-6 shadow-lg">
                    <div className="flex flex-col space-y-4">
                        <h2 className="text-2xl font-semibold ml-2">Storage</h2>

                        {/* Title Row */}
                        <div className="flex p-4 rounded-md shadow-md" style={{ backgroundColor: "#f4f1de" }}>
                            <div className="flex-1 font-bold">S.no</div>
                            <div className="flex-1 font-bold">Item</div>
                            <div className="flex-1 font-bold mr-7">Quantity (kgs)</div>
                        </div>

                        {/* Data Rows */}
                        {items.map((item, index) => (
                            <div key={index} className="flex bg-gray-200 p-4 rounded-md shadow-md" style={{ backgroundColor: "#FFFEF5" }}>
                                <div className="flex-1">{index + 1}</div>
                                <div className="flex-1">{item.name}</div>
                                <div className="flex-1">{item.quantity}</div>
                                <IoMdClose
                                    style={{ fontSize: 25, opacity: 0.5, cursor: 'pointer' }}
                                    onMouseEnter={(e) => e.target.style.color = 'red'}
                                    onMouseLeave={(e) => e.target.style.color = 'black'}
                                    onClick={() => handleRemoveItem(index)}
                                />
                            </div>
                        ))}

                        {/* Input Fields for new item */}
                        <div className="flex flex-col bg-gray-100 p-4 rounded-md shadow-md">
                            <div className="flex">
                                <input
                                    type="text"
                                    className="flex-1 border rounded-md p-2 mr-2"
                                    placeholder="Item name"
                                    value={newItem.name}
                                    onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
                                />
                                <input
                                    type="number"
                                    step="0.01" // Allow decimals
                                    className="flex-1 border rounded-md p-2 mr-2"
                                    placeholder="Quantity (kgs)"
                                    value={newItem.quantity}
                                    onChange={(e) => setNewItem({ ...newItem, quantity: e.target.value })}
                                />
                                <button
                                    type="submit"
                                    className="bg-green-800 text-white py-2 px-4 rounded-lg hover:bg-green-900"
                                    onClick={handleAddItem}
                                >
                                    Add
                                </button>
                            </div>

                            {/* Error Message below input fields */}
                            {error && (
                                <div className="text-red-600 text-sm mt-2">
                                    {error}
                                </div>
                            )}
                        </div>

                        {/* Submit Button */}
                        <div className='flex justify-between mt-4'>
                            <button
                                type="submit"
                                className="w-24 self-end bg-blue-800 text-white py-2 rounded-lg hover:bg-blue-900"
                                onClick={handleSubmit}
                            >
                                Enter
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Storage;
