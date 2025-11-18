import './App.css'
import { SchoolCombobox } from '@/components/school-combobox/school-combobox'
import { Navbar } from '@/components/navbar'
import { HouseDecoration } from '@/components/house-decoration'

function App() {
  return (
    <>
      <Navbar />
      <div>
        <a href="https://react.dev" target="_blank">
        </a>
      </div>
      <h1 className="tagline">Find a lease <strong><em>seriously</em></strong> fast</h1>
      <div className="card">
        <SchoolCombobox />
      </div>
      <HouseDecoration />
    </>
  )
}

export default App

