import { Navigate } from "react-router-dom";
import Navbar from "./Navbar";

export default function ProtectedRoute({children}){
    const token = localStorage.getItem('access')

    if (!token){
        return <Navigate to ='/login'/>
    }
    return (
        <> {/*Fragment since react component can only return one element*/}
    <Navbar/>
    {children}
    </>
    )
}