import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import { Editor } from "@monaco-editor/react"
import api from "../api/axios"

export default function Problem_Detail(){
    const {id} = useParams()
    const [problem,setProblem] = useState(null)
    const [language,setLanguage] = useState('python')
    const[code, setCode] =useState('')


    useEffect(() =>{
        api.get(`/problems/${id}/`)
        .then(res =>setProblem(res.data))
        .catch(err=>console.log(err))
    }, [id])

    const handelsubmit = () =>{
        api.post(`/submissions/problem/${id}/`,{
            code:code,
            language:language,
            problem: id
        })
        .then(res =>{
            console.log(res.data)
            setTimeout(() =>{
                api.get(`/submissions/problem/${id}/`)
                .then(r => console.log(r.data.results[id]))
            }, 3000)
        })
        }

    if (!problem) return <div className="text-white">Loading...</div>
    return(
         <div className="min-h-screen bg-gray-950 p-8">
            <h1 className="text-3xl font-bold text-white mb-4">{problem.title}</h1>
            <span className="text-gray-400">{problem.difficulty}</span>
            <p className="text-gray-300 mt-6">{problem.description}</p>
            <select
                value = {language}
                onChange={(e) => setLanguage(e.target.value)}
                className = "bg-gray-800 text-white px-4 py-2 rounded-lg mb-4"
                >
                    <option value = "python">Python</option>
                    <option value="cpp">C++</option>
                    <option value="c">C</option>
                </select>
            <Editor
                height = '400px'
                language = {language}
                theme = 'vs-dark'
                defaultValue='Write your code here'
                onChange={(value) => setCode(value)}
                />
                <button onClick={handelsubmit} className="mt-4 bg-indigo-600 text-white px-6 py-2 cursor pointer hover:bg-indigo-500 rounded-lg">Submit</button>
        </div>
    )
}