import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import React from 'react'
import IndexPage from "./pages/IndexPage"
import './App.css'

const App = () => {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<IndexPage />} />
      </Routes>
    </Router>
  )
}

export default App;