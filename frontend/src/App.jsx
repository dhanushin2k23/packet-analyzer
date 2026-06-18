import { lazy, Suspense } from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";

const Security = lazy(() => import("./components/Security"));
const Login = lazy(() => import("./pages/Login"));
const Register = lazy(() => import("./pages/Register"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Upload = lazy(() => import("./pages/Upload"));
const Report = lazy(() => import("./pages/Report"));


function App(){


return (

<BrowserRouter>

<Suspense fallback={<div className="auth-page">Loading...</div>}>

<Routes>


<Route path="/" element={<Login/>}/>


<Route path="/register" element={<Register/>}/>


<Route path="/dashboard" element={<Dashboard/>}/>


<Route path="/upload" element={<Upload/>}/>


<Route path="/report/:id" element={<Report/>}/>

<Route path="/security" element={<Security/>}/>


</Routes>

</Suspense>


</BrowserRouter>


)

}


export default App;
