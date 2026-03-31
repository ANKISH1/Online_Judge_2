import { useState } from "react"
import api from "../api/axios"
import { useNavigate } from "react-router-dom"

export default function Register(){
    const[formData, SetFormData] = useState({
        'username':'',
        'email':'',
        'password':''

    })
    const navigate = useNavigate()

    const handlechange = (e) =>{
        SetFormData({...formData, [e.target.name]:e.target.value})
    }
    const handelsubmit =async (e)=>{
        e.preventDefault()
        try{
            api.post('/auth/register/', formData)
            .then(res => console.log(res.data))
            navigate('/login')
        }
        catch(err){
            console.log(err.response.data)
        }
    }
    
    return (
        <div className="min-h-screen bg-gray-950 flex items-center justify-center">
            <div className="bg-gray-800 p-8 rounded-2xl w-full max-w-md">
                <h1 className="text-3xl font-bold text-white mb-8">Register</h1>
                <div className="space-y-5">
                    <input
                    name = "username"
                    type = "text"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handlechange}
                    className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-3"
                    />
                    <input
                    name = "email"
                    type = "email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handlechange}
                    className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-3"
                    />
                    <input
                    name = "password"
                    type = "password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handlechange}
                    className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-3"
                    />
                    <button onClick={handelsubmit} className="w-full bg-indigo-600 text-white font-semibold py-3 rounded-lg">Register</button>
                </div>
            </div>
        </div>
    )
}