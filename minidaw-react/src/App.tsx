import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import MiniDAWIntegrated from './components/MiniDAWIntegrated'
import ClonedVoicesLibrary from './components/ClonedVoicesLibrary'
import VoiceCloning from './components/VoiceCloning'
import NewsAutoPostUltraSimple from './components/NewsAutoPostUltraSimple'
import { Toaster } from './components/ui/toaster'
import './index.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Routes>
          <Route path="/" element={<MiniDAWIntegrated />} />
          <Route path="/minidaw" element={<MiniDAWIntegrated />} />
          <Route path="/cloned-voices" element={<ClonedVoicesLibrary />} />
          <Route path="/voice-cloning" element={<VoiceCloning />} />
          <Route path="/news" element={<NewsAutoPostUltraSimple />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        <Toaster />
      </div>
    </Router>
  )
}

export default App
