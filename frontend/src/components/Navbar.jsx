import { useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <nav className="bg-gray-900 px-8 py-4 flex justify-between items-center">
      <span 
        onClick={() => navigate('/problems')} 
        className="text-white font-bold text-xl cursor-pointer"
      >
        RadiantOJ
      </span>
      
      <div className="flex gap-6">
        <span onClick={() => navigate('/problems')} className="text-gray-300 cursor-pointer hover:text-white">Problems</span>
        <span onClick={() => navigate('/submissions')} className="text-gray-300 cursor-pointer hover:text-white">Submissions</span>
        <span onClick={handleLogout} className="text-red-400 cursor-pointer hover:text-red-300">Logout</span>
      </div>
    </nav>
  )
}