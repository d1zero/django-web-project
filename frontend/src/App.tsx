import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Footer from './components/Footer/Footer'
import Navbar from './components/Navbar/Navbar'
import MainPage from './pages/MainPage/MainPage'
import NotFound from './pages/NotFound/NotFound'


function App() {
    return (
        <>
            <Navbar />
            <Routes>
                <Route path='/' element={<MainPage />} />
                <Route path='*' element={<NotFound />} />
            </Routes>
            <Footer />
        </>
    )
}

export default App
