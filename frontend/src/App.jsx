import {BrowserRouter, Routes, Route} from "react-router-dom";
import Security from "./components/Security";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Report from "./pages/Report";


function App(){


return (

<BrowserRouter>

<Routes>


<Route path="/" element={<Login/>}/>


<Route path="/register" element={<Register/>}/>


<Route path="/dashboard" element={<Dashboard/>}/>


<Route path="/upload" element={<Upload/>}/>


<Route path="/report/:id" element={<Report/>}/>

<Route path="/security" element={<Security/>}/>


</Routes>


</BrowserRouter>


)

}


export default App;