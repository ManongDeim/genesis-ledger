import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"
import ForgotPassword from "./pages/ForgotPassword"
import Login from "./pages/login"
import Register from "./pages/register"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
