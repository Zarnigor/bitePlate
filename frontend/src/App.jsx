import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard   from './pages/Dashboard'
import Tables      from './pages/Tables'
import Orders      from './pages/Orders'
import Kitchen     from './pages/Kitchen'
import Menu        from './pages/Menu'
import Billing     from './pages/Billing'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/"        element={<Dashboard />} />
        <Route path="/tables"  element={<Tables />}    />
        <Route path="/orders"  element={<Orders />}    />
        <Route path="/kitchen" element={<Kitchen />}   />
        <Route path="/menu"    element={<Menu />}      />
        <Route path="/billing" element={<Billing />}   />
      </Routes>
    </Layout>
  )
}
