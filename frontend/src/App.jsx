import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Dashboard from './pages/Dashboard';
import Login from '/Users/akashbalaji/Desktop/Fruit_SpoilDetection/frontend/src/pages/Login.jsx';
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
