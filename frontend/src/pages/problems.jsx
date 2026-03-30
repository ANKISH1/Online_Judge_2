import { useState, useEffect } from "react"
import api from "../api/axios"



export default function Problems(){

    const [problems, setProblems] = useState([])

    useEffect(() =>{
        api.get('/problems/')
        .then(res =>setProblems(res.data.results))
        .catch(err =>console.log(err))
    },[])

    console.log(problems)

    return(
        <div className="min-h-screen bg-gray-950 p-8">

        <h1 className="text-3xl font-bold text-white mb-8">

            Problems Page
        </h1>
        {problems.map((p) =>(
        <div key={p.id} className="bg-gray-800 p-4 rounded-lg mb-3">
            <span className="text-white">{p.title}</span>
            <span className="text-gray-400 ml-4">{p.difficulty}</span>

        </div>
       ))}
        </div>
    )
}