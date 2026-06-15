import { useNavigate } from "react-router-dom";
import {
  LogOut,
  Upload,
  LayoutDashboard
} from "lucide-react";


function Navbar(){


const navigate = useNavigate();



const logout = ()=>{

localStorage.removeItem("token");

navigate("/");

};



return (

<div className="navbar">



<div className="nav-left">


<h2>
Packet Analyzer
</h2>


</div>





<div className="nav-right">



<button
onClick={()=>navigate("/dashboard")}
>

<LayoutDashboard size={18}/>

Dashboard

</button>





<button
onClick={()=>navigate("/upload")}
>

<Upload size={18}/>

Upload

</button>





<button
onClick={logout}
>


<LogOut size={18}/>

Logout


</button>




</div>




</div>

)


}


export default Navbar;