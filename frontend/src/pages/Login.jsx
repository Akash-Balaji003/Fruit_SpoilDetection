import React, { useState } from 'react';
import {useNavigate} from 'react-router-dom';

import background from '/Users/akashbalaji/Desktop/Fruit_SpoilDetection/frontend/src/assets/BG_Random2.png';


function Login() {
    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [passcode, setPasscode] = useState('');
    const [errors, setErrors] = useState({ username: '', passcode: '' });

    const handleSubmit = (e) => {
        e.preventDefault();

        let formIsValid = true;
        const newErrors = { username: '', passcode: '' };

        if (!username) {
            formIsValid = false;
            newErrors.username = 'Username is required';
        }

        if (!passcode) {
            formIsValid = false;
            newErrors.passcode = 'Passcode is required';
        }

        if (username === 'Admin' && passcode === 'Admin') {
            navigate('/dashboard');
          } else {
            setErrors('Invalid username or password'); 
        }

        setErrors(newErrors);

        if (formIsValid) {
            // Form is valid, you can perform further actions (e.g., API call)
            console.log('Form submitted:', { username, passcode });
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center w-full absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url(${background})`, backgroundColor: 'rgba(0, 0, 0, 0.2)', /* Dark overlay color */
        backgroundBlendMode: 'overlay'}}>

            {/* Header */}
            <header className="absolute top-0 left-0 right-0 px-10 py-4 bg-transparent flex justify-between items-center">
                <div className="text-4xl font-bold text-gray-800">Frutech</div>
            </header>

            {/* Login Form */}
            <div className="relative z-10 bg-white bg-opacity-90 rounded-lg shadow-lg p-8 w-full max-w-md mx-auto" >
                <h2 className="text-2xl font-semibold text-center mb-6">Login</h2>

                <form onSubmit={handleSubmit}>
                    
                    {/* Username Input */}
                    <div className="mb-4">
                        <label className="block text-gray-700">Username</label>
                        <input
                            type="text"
                            className={`w-full px-4 py-2 mt-2 rounded-lg bg-gray-200 border ${errors.username ? 'border-red-500' : 'focus:border-gray-400'} focus:outline-none`}
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                        />
                        {errors.username && (
                            <span className="text-red-500 text-sm">{errors.username}</span>
                        )}
                    </div>

                    {/* Passcode Input */}
                    <div className="mb-4">
                        <label className="block text-gray-700">Password</label>
                        <div className="relative">
                            <input
                                type="password"
                                className={`w-full px-4 py-2 mt-2 rounded-lg bg-gray-200 border ${errors.passcode ? 'border-red-500' : 'focus:border-gray-400'} focus:outline-none`}
                                value={passcode}
                                onChange={(e) => setPasscode(e.target.value)}
                                placeholder="Enter your passcode"
                            />
                            <span className="absolute inset-y-0 right-0 pr-3 flex items-center">
                                <i className="fas fa-eye text-gray-500"></i> {/* Replace with icon */}
                            </span>
                        </div>
                        {errors.passcode && (
                            <span className="text-red-500 text-sm">{errors.passcode}</span>
                        )}
                    </div>

                    {/* Forgot Passcode Link */}
                    <div className="text-right mb-4">
                        <a href="#" className="text-gray-600 hover:text-blue-500">
                            Forgot password?
                        </a>
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="w-full bg-blue-800 text-white py-2 rounded-lg hover:bg-blue-900"
                        onClick={() => handleSubmit}
                    >
                        LOGIN
                    </button>

                    {/* Create Account Link */}
                    <div className="mt-4 text-center">
                        <a href="#" className="text-gray-600 hover:text-blue-500">
                            New here? Create an account
                        </a>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Login;
