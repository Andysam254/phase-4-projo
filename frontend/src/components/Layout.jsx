import React from 'react'
import Navbar from "../components/Navbar"
import Footer from "../components/Footer"
import { Outlet } from 'react-router-dom'


export default function Layout() {
  return (
    <div>
      <Navbar/>
      
      <div className="min-h-[90vh] bg-gray-200 container mx-auto p-8">
         <Outlet />
      </div>

      <Footer />
      
    </div>
  )
}
