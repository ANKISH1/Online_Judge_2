import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import { Editor } from "@monaco-editor/react"
import api from "../api/axios"

export default function Problem_Detail(){
    const {id} = useParams()
    const [problem,setProblem] = useState(null)
    const [language,setLanguage] = useState('python')
    const[code, setCode] =useState('')
    const[customInput,setCustomInput] = useState('')
    const[output, setOutput] = useState('')
    const[verdict,setVerdict] = useState(null)
    const [isSubmitting, setIsSubmitting] = useState(false)
    const [hint, setHint] = useState('')
    const [isHinting, setisHinting]  = useState(false)




    useEffect(() =>{
        api.get(`/problems/${id}/`)
        .then(res =>setProblem(res.data))
        .catch(err=>console.log(err))
    }, [id])

    const handelsubmit = () =>{
        setVerdict(null)
        setIsSubmitting(true)


        api.post(`/submissions/problem/${id}/`,{
            code:code,
            language:language,
            problem: id
        })
        .then(res =>{
            const submissionId = res.data.id

            console.log(res.data)
            const interval = setInterval(() =>
            api.get(`/submissions/${submissionId}/`)
            .then(r=>{
                if(r.data.verdict!=='PENDING'){
                    setVerdict(r.data.verdict)
                    setIsSubmitting(false)
                    clearInterval(interval)
                }
            }))
        })
        }
    const handlerun = () =>{
        api.post('/judge/run/',{
            code: code,
            language:language,
            input: customInput
        })
        .then(res => setOutput(res.data.output))
        .catch(err =>console.log(err))
    }
    
    const handlehint = () => {
        setisHinting(true)
        api.post(`/problems/${id}/hint/`,{
            user_code: code
        })
        .then(res => {
            setHint(res.data.hint)
            setisHinting(false)
        })
        .catch(err => {
            console.log(err)
            setisHinting(false)

    })

    }

    if (!problem) return <div className="text-white">Loading...</div>
    return(
         <div className="min-h-screen bg-gray-950 p-8">


            {/* Problem Info */}
            <h1 className="text-3xl font-bold text-white mb-4">{problem.title}</h1>
            <span className="text-gray-400">{problem.difficulty}</span>
            <p className="text-gray-300 mt-6">{problem.description}</p>

            {/* Language Dropdown */}
            <select
                value = {language}
                onChange={(e) => setLanguage(e.target.value)}
                className = "bg-gray-800 text-white px-4 py-2 rounded-lg mb-4"
                >
                    <option value = "python">Python</option>
                    <option value="cpp">C++</option>
                    <option value="c">C</option>
                </select>

            {/*Editor*/}    
            <Editor
                height = '300px'
                language = {language}
                theme = 'vs-dark'
                defaultValue='Write your code here'
                onChange={(value) => setCode(value)}
                />

            {/*Input*/}    
            <textarea
                value = {customInput}
                onChange={(e) => setCustomInput(e.target.value)}
                placeholder="Write your custom input here..."
                className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-3 mt-4"
                rows={3}
                />

            {/*Buttons*/} 
            <div className="flex gap-4 mt-4"> 
            <button
                onClick={handlerun}
                className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-500">
                    Run
            </button>


            <button onClick={handelsubmit} className="mt-4 bg-indigo-600 text-white px-6 py-2 cursor pointer hover:bg-indigo-500 rounded-lg">
                    Submit
            </button>

            <button onClick={handlehint} className="mt-4 bg-orange-600 text-white px-6 py-2 cursor pointer hover:bg-orange-500 rounded-lg">
                    Hint
            </button>

            </div>

            {/*Output*/}

            {output && (
                    <div className="mt-4 bg-gray-800 text-white p-4 rounded-lg">
                    <pre>{output}</pre>
                    </div>
            )}

            {/*Verdict*/}

            {isSubmitting && <p className="text-white">Evaluating...</p>}
            {verdict&&(
                <p style={{color:verdict==='ACCEPTED'?'green':'red'}}>{verdict}</p>
            )}

            {/*hint*/}
            {isHinting && <p className="text-white">Getting hint...</p>}
            {hint && (
                <div className="mt-4 text-white p-4 rounded-lg">
                <p className="whitespace-pre-wrap break-words">{hint}</p>
                    </div>
            )}

        </div>
    )
}