import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import SignIn from "./SignIn"
import Drive from "./Drive"
function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<SignIn />}></Route>
                <Route path="/drive" element={<Drive />}></Route>
            </Routes>
        </Router>
    );
}

export default App;
