import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout"
import Home from "./pages/Home"
import Login from "./pages/Login"
import NoPage from "./pages/NoPage"
import Freelancers from './pages/Freelancers';
import Jobs from './pages/Jobs';



function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="login" element={<Login />} />
          <Route path="freelancers" element={<Freelancers />} />
          <Route path="jobs" element={<Jobs />} />
          <Route path="*" element={<NoPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
