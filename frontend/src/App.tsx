import { Container, CssBaseline, LinearProgress } from '@mui/material'
import React, { useContext } from 'react'
import { Routes, Route } from 'react-router-dom'
import Footer from './components/Footer/Footer'
import Navbar from './components/Navbar/Navbar'
import MainPage from './pages/MainPage/MainPage'
import NotFound from './pages/NotFound/NotFound'
import GenresListPage from './pages/GenresListPage/GenresListPage'
import { observer } from 'mobx-react-lite'
import { Context } from './main'

function App() {
    const { store } = useContext(Context)
    return (
        <>
            <Navbar />
            <CssBaseline />
            {
                store.loading
                    ? <LinearProgress color="secondary" />
                    : null
            }
            <Container maxWidth="lg">
                <Routes>
                    <Route path='/' element={<MainPage />} />
                    <Route path='/genres' element={<GenresListPage />} />
                    <Route path='*' element={<NotFound />} />
                </Routes>
            </Container>
            <Footer />
        </>
    )
}

export default observer(App)
