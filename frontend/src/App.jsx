import { BrowserRouter, Routes, Route , Navigate} from "react-router-dom";
import Login from "./pages/login";
import Problems from "./pages/problems";

export default function App(){
  return(
    <BrowserRouter>
    <Routes>
      <Route path = "/" element = {<Navigate to = "/login"/>}/> //Redirect on Render
      <Route path = "/login" element = {<Login/>}/>
      <Route path = "/problems" element = {<Problems/>}/>
    </Routes>
    </BrowserRouter>
  )
}