import { BrowserRouter, Routes, Route , Navigate} from "react-router-dom";
import Login from "./pages/login";
import Problems from "./pages/problems";
import Problem_Detail from "./pages/problem_detail";
import Submissions from "./pages/submissions";
import Register from "./pages/register";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/Navbar";

export default function App(){
  return(
    <BrowserRouter>
    <Routes>
      <Route path = "/" element = {<Navigate to = "/login"/>}/> //Redirect on Render
      <Route path = "/login" element = {<Login/>}/>
      <Route path = "/register" element = {<Register/>}/>
      <Route path = "/problems" element = {
        <ProtectedRoute>
        <Problems/>
        </ProtectedRoute>}/>
      <Route path = "/problems/:id" element = {<Problem_Detail/>}/>
      <Route path = "/submissions" element = {
        <ProtectedRoute>
        <Submissions/>
        </ProtectedRoute>
        }/>
    </Routes>
    </BrowserRouter>
  )
}