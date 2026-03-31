import { useState, useEffect } from "react"
import api from "../api/axios"

export default function Submissions(){

    const[submissions, setSubmissions] = useState([])

    useEffect(()=>{
        api.get('/submissions/')
        .then(res =>setSubmissions(res.data.results))
        .catch(err => console.log(err))
    },[])
    console.log(submissions)

    return (
        <div className="min-h-screen bg-gray-950 p-8">
            <h1 className=" text-3xl font-bold text-white mb-8">Submissions</h1>
                {submissions.map((s) =>(
                    <div key={s.id} className="bg-gray-800 p-4 rounded-lg mb-3 flex gap-4">
                        <span className="text-white">{s.problem_title}</span>
                        <span className="text-white">{s.language}</span>
                        <span className="text-gray-400">{s.verdict}</span>
                    </div>

                ))}
        </div>
    )
}