import './App.css';
import { 
  BrowserRouter as Router, 
  Route, 
  Routes 
} from 'react-router-dom';
import RegistrationPage from './pages/registration';
import DashboardPage from './pages/dashboard';
import RiskPage from './pages/risks';
import WeightPage from "./pages/weights.tsx";
import Menubar from './components/navbar';

function App() {

  return (
    <Router>
      <Menubar />
      <Routes>      
        <Route path='/' element={<RegistrationPage />} />
        <Route path='/dashboard' element={<DashboardPage />} />
        <Route path='/customers/risks/:id' element={<RiskPage />} />
        <Route path='/admin/weights' element={<WeightPage />} />
      </Routes>    
    </Router>
  )
}

export default App
