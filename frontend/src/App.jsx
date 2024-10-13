import { useState } from 'react'

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Dashboard from './pages/Dashboard';
import Login from './pages/login';
import Storage from './pages/Storage';

function App() {

  return (
	<Router>
		<Routes>
			<Route path="/" element={<Login />} />
			<Route path="/dashboard" element={<Dashboard />} />
			<Route path="/storage" element={<Storage />} />
		</Routes>
	</Router>
  )
}

export default App
