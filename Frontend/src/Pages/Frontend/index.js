import React from 'react'
import { Route, Routes } from 'react-router-dom'
import BotPage from './BotPage'
import Footer from 'Components/Footer/Footer'

export default function Frontend() {
  return (
    <>
      <Routes>
        <Route path="/" element={<BotPage />} />
      </Routes>
      <Footer />
    </>
  )
}
